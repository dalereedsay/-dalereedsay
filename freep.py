# coding: utf-8
#what the hell is this shit!!!
from HTMLParser import HTMLParser
from urllib2 import urlopen
import re
import twitter
import argparse

#why are there so many of these whoever thought of this should be executed!!!!!
parser = argparse.ArgumentParser()
parser.add_argument('--consumer_key')
parser.add_argument('--consumer_secret')
parser.add_argument('--access_token_key')
parser.add_argument('--access_token_secret')
args = parser.parse_args()



class Freep(HTMLParser):
	current = dict()
	stack = []
	comments = []
	found_old_tweet = 0
	
	api = twitter.Api(consumer_key=args.consumer_key, consumer_secret=args.consumer_secret,
	                    access_token_key=args.access_token_key, access_token_secret=args.access_token_secret,
	                    input_encoding=None)
	oldTweets = api.GetUserTimeline('dalereedsay')
	
	def __init__(self, url):
		HTMLParser.__init__(self)
		self.data = list()
		req = urlopen(url)
		self.feed(req.read())


	def handle_starttag(self, tag, attrs):
		#inside a damn comment block!!
		if self.stack and self.stack[0]['tag'] == 'li':
			self.stack.append({'tag': tag, 'attrs': attrs, 'data': ''})
		
		#freep comments start in a god damn <li class="comment "
		if tag == 'li' and len(self.stack) == 0 and attrs and attrs[0][1] == 'comment ':
			self.stack.append({'tag':tag})
			current = dict()
	

	def handle_endtag(self, tag):
		#pop tags off the stack for the current comment!!
		#if you can't follow this you are a moron!!!
		if len(self.stack) > 0:
			item = self.stack.pop()
			
			#if item['tag'] != tag:
				#print "ffffffffffffffff"
			
			if item['tag'] == 'div' and item['attrs'][0][0] == 'class' and item['attrs'][0][1] == 'text':
				if 'comment' in self.current:
					self.current['comment'] = "{0} {1}".format(self.current['comment'], item['data']).strip()
				else:
					self.current['comment'] = item['data'].strip()
			
			if item['tag'] == tag == 'p':
				if 'comment' in self.current:
					self.current['comment'] = "{0} {1}".format(self.current['comment'], item['data']).strip()
				else:
					self.current['comment'] = item['data'].strip()
					

					
			if item['tag'] == tag == 'span':
				self.current['date'] = item['data']
				
			if item['tag'] == tag == 'a' and item['data'] == 'Post Reply':
				href = item['attrs'][1][1]
				search = re.search('id=([0-9]{7}),([0-9]+)', href)
				
				self.current['thread'] = search.group(1)
				self.current['post'] = search.group(2)
				
			#if the stack is empty its obamas fault!!
			if item['tag'] == 'li':
				if 'comment' in self.current and 'post' in self.current and 'thread' in self.current:
					#print self.current
					self.comments.append(self.current)
					#self.do_tweet(self.current)
				self.current = dict()
			
		#done with this shit
		if tag == 'html':
			print "fuck you, got html"
			self.delete_existing()
			while len(self.comments) > 0:
				self.do_tweet(self.comments.pop())
				
			
	def handle_data(self,data):
		#this gets the crap between matching tags!! idiot!!!
			if len(data.strip()) and self.stack:
				index = len(self.stack) -1
				self.stack[index]['data'] = "{0}{1}".format(self.stack[index]['data'], data)

	def handle_charref(self,charcode):
		index = len(self.stack) -1
		if self.stack and self.stack[index]:
			#print "got code: %s" % charcode
			if charcode == '8217' or charcode == '146':
				charcode = "'"
			elif charcode == '8220':
				charcode = '"'
			elif charcode == '8221':
				charcode = '"'
			else:
				charcode = "&{0};".format(charcode)
			self.stack[index]['data'] = "{0}{1}".format(self.stack[index]['data'], charcode)
	
	
	def do_tweet(self, dict):
		#if the tweet is too long break it up!! assmöde
		if len(dict['comment']) > 125:
			lines = re.findall('(.+?[\n\.\?!]+)+?',dict['comment'])
		else:
			lines = [dict['comment']]
	
		for t in lines:
			if len(t) > 10:
				if t[0] == '"' and t[len(t)-1] == '"':
					i = 1
				else:
					tweet = "{0} #FR{1} :{2}".format(t,dict['thread'],dict['post']).strip()
					if len(tweet) <= 140:
						print "tweeting %s" % tweet
						#status = self.api.PostUpdate(tweet)
 
	def delete_existing(self):
		mostRecentOldTweet = self.oldTweets[0].text
		#print "most recent: %s" % mostRecentOldTweet[0:len(mostRecentOldTweet)-15]
        
		index = -1
		for i in range(len(self.comments)):
			#print "checking %s" % self.comments[i]['comment']
			if self.comments[i]['comment'].find(mostRecentOldTweet[0:len(mostRecentOldTweet)-15]) > -1:
				index = i
				#print "found old index %s" % index
				break
				
		del self.comments[index:len(self.comments)]

		
		
		
		


Freep('file:///Users/me/Desktop/test.html')
#Freep('http://www.freerepublic.com/tag/by:dalereed/index?brevity=full;tab=comments')
					