from tweeter import Tweeter
from freep import Freep
from keys import Keys


dalereedsay = Tweeter('dalereedsay',Keys.dalereedsay())
dalereed = Freep('dalereed', dalereedsay.mostRecent())
#print "dalereed comments:{0}".format(dalereed.newComments())
dalereedsay.postList(dalereed.newComments())
#dalereedsay.postList(dalereed.newMentions())

jimrobsay = Tweeter('jimrobsay', Keys.jimrobsay())
jimrob = Freep('jimrobinson', jimrobsay.mostRecent())
#print "jimrob comments:{0}".format(jimrob.newComments())
jimrobsay.postList(jimrob.newComments())
#jimrobsay.postList(jimrob.newMentions())


