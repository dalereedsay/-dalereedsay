# coding: utf-8
#what the hell is this shit!!!
from HTMLParser import HTMLParser
from urllib2 import urlopen
import re


class Mentions(HTMLParser):
	current = dict()
	tagStack = []
	comments = []
	item = None
	tweeter = None
	
	#url = 'file:///Users/me/Desktop/test.html'
	url = 'http://www.freerepublic.com/focus/news/{0}/posts?page={1}#{1}'
	

	def __init__(self, item):
		HTMLParser.__init__(self)
		self.data = list()
		self.item = item
		
		req = urlopen(self.url.format(item['list'][0], item['list'][1]))
		self.feed(req.read())


	def handle_starttag(self, tag, attrs):
		#inside a damn comment block!!
		if self.tagStack and self.tagStack[0]['tag'] == 'li':
			self.tagStack.append({'tag': tag, 'attrs': attrs, 'data': ''})
		
		#freep comments start in a god damn <li class="comment "
		if tag == 'li' and len(self.tagStack) == 0 and attrs and attrs[0][1] == 'comment ':
			self.tagStack.append({'tag':tag})
			current = dict()
	

	def handle_endtag(self, tag):
		#pop tags off the tagStack for the current comment!!
		#if you can't follow this you are a moron!!!
		if len(self.tagStack) > 0:
			item = self.tagStack.pop()
			
			#if item['tag'] != tag:
				#print "ffffffffffffffff"
			
			if item['tag'] == 'div' and item['attrs'][0][0] == 'class' and item['attrs'][0][1] == 'text':
				if not 'comment' in self.current:
					self.current['comment'] = []
					
				self.current['comment'].append(item['data'].strip())
			
			if item['tag'] == tag == 'p':
				if not 'comment' in self.current:
					self.current['comment'] = []
					
				self.current['comment'].append(item['data'].strip())
					

					
			if item['tag'] == tag == 'span':
				self.current['date'] = item['data']
				
			if item['tag'] == tag == 'a' and item['data'] == 'Post Reply':
				href = item['attrs'][1][1]
				search = re.search('id=([0-9]{7}),([0-9]+)', href)
				
				self.current['thread'] = search.group(1)
				self.current['post'] = search.group(2)
				
			#if the tagStack is empty its obamas fault!!
			if item['tag'] == 'li':
				if 'comment' in self.current and 'post' in self.current and 'thread' in self.current:
					self.check_current()
				self.current = dict()
			
		#done with this shit
		if tag == 'html':
			print "fuck you, got html"
			#self.delete_existing()
			#while len(self.comments) > 0:
			#	self.build_tweet(self.comments.pop())
				
			
	def handle_data(self,data):
		#this gets the crap between matching tags!! idiot!!!
			if len(data.strip()) and self.tagStack:
				index = len(self.tagStack) -1
				self.tagStack[index]['data'] = "{0}{1}".format(self.tagStack[index]['data'], data)

	def handle_charref(self,charcode):
		index = len(self.tagStack) -1
		if self.tagStack and self.tagStack[index]:
			#print "got code: %s" % charcode
			if charcode == '8217' or charcode == '146':
				charcode = "'"
			elif charcode == '8220':
				charcode = '"'
			elif charcode == '8221':
				charcode = '"'
			else:
				charcode = "&{0};".format(charcode)
			self.tagStack[index]['data'] = "{0}{1}".format(self.tagStack[index]['data'], charcode)
	
	
	def check_current(self):
		mr = self.tweeter.mostRecent()
		#print "{0} == {1}".format(mr, self.current['comment'][0])
		t = self.current['thread']
		p = self.current['post']
		
		if mr.find("#FR{0} :{1}".format(t,p)) > 0:
			#print "found old"
			raise AssertionError("found old tweet")
		else:
			#print "found new"
			self.comments.append(self.current)
	
	def newComments(self):
		return self.comments
					