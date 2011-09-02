# coding: utf-8
import twitter
import re
import sys



class Tweeter:
	api = None
	valid = False
	oldTweets = []
	mentions = []
	account = None
	
	def __init__(self, account, keys):
		try:
			self.api = twitter.Api(consumer_key=keys['consumer_key'], consumer_secret=keys['consumer_secret'],
			                    access_token_key=keys['access_token_key'], access_token_secret=keys['access_token_secret'],
			                    input_encoding=None)
			self.account = account
			self.oldTweets = self.api.GetUserTimeline(self.account, 1, None)
			#print "oldtweets {0}:{1}".format(account, self.oldTweets[0])
			self.valid = True
		except:
			print "twitter api error:", sys.exc_info()[0]
			self.valid = False
			
	def getMentions(self):
		self.mentions = []
		list = self.api.GetMentions()
		
		for i in range(len(list)):
			self.parseMentionTweet(list[i])
		
		return self.mentions
		
			
	def parseMentionTweet(self, status):
		if status.text.find('RT') >= 0:
			#fuck retweets who cares
			print "fuck retweets"
			return
			
		if not status.text.find('@{0}'.format(self.account)) == 0:
			#should start with @dalereedsay
			print "fuck that one, not starting with @{0}".format(self.account)
			return
			
		list = re.findall("([0-9]{7}):([0-9]+)", status.text)
		if len(list) > 0:
			self.mentions.append({'list':list, 'status':status})
		
	
		
	def mostRecent(self):
		if self.valid:
			print "{0} most recent: {1}".format(self.account, self.oldTweets[0].text)
			return self.oldTweets[0].text
		else:
			print self.oldTweets[0].text
			raise ValueError("ok wtf")
			
	def postList(self,list):
		while len(list) > 0:
			self.build_tweet(list.pop())
	
	def build_tweet(self, dict):
		#if the tweet is too long break it up!! assmöde
		lines = dict['comment']
		
		build_tweet = ''
		for t in lines:
			if len(t) == 0:
				continue
				
			if t[0] == '"' and t[len(t)-1] == '"':
				#skippin quotes
				continue
				
			if len(build_tweet) + len(t) < 125:
				build_tweet = "{0} {1}".format(build_tweet,t)
				
			else:
				self.send_tweet(build_tweet,dict['thread'],dict['post'])
				build_tweet = t
		
		#print last one		
		self.send_tweet(build_tweet,dict['thread'],dict['post'])
		
	def send_tweet(self,text,thread,post):
		if len(text) > 2 and len(text) < 125:
			build_tweet = "{0} #FR{1} :{2}".format(text,thread,post).strip()
			print "({0}) tweeting [ {1} ]".format(self.account,build_tweet)
			status = self.api.PostUpdate(build_tweet)

