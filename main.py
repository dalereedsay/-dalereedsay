from tweeter import Tweeter
from freep import Freep
import argparse

#why are there so many of these whoever thought of this should be executed!!!!!
parser = argparse.ArgumentParser()
parser.add_argument('--consumer_key')
parser.add_argument('--consumer_secret')
parser.add_argument('--access_token_key')
parser.add_argument('--access_token_secret')
args = parser.parse_args()


tweeter = Tweeter(args)
freep = Freep(tweeter)

newComments = freep.newComments()
tweeter.postList(newComments)
