from tasks import *

def crawl():
	isbn =  ISBN.find({'isbn_13':{'$exists':1}},{'_id':0})
	for e in isbn:
		for h in e.values():
			for t in h:
				var = Details.find_one({'_id':t})
				if (var == None):
					get_detail.delay(t)
					print 'got it ', t
                    

crawl()
