# coding: utf-8
import twitter
import argparse



class Tweeter:
	api = None
	valid = False
	oldTweets = []
	
	def __init__(self, args):
		try:
			self.api = twitter.Api(consumer_key=args.consumer_key, consumer_secret=args.consumer_secret,
			                    access_token_key=args.access_token_key, access_token_secret=args.access_token_secret,
			                    input_encoding=None)
			self.oldTweets = self.api.GetUserTimeline('dalereedsay')
			self.valid = True
		except:
			print "error"
			self.valid = False
			
	def mostRecent(self):
		if self.valid:
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
			if len(t) < 5:
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
			print "Tweeting >>> %s <<<" % build_tweet
			status = self.api.PostUpdate(build_tweet)

