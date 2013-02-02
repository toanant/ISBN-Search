from tasks import *

def crawl():
	
	for category in CATEGORIES:
		isbn =  RISBN.find({category:{'$exists':1}},{'_id':0})
		for t in isbn:
		k = t.values()
		isbn = k[0]
		size = len(isbn)
		while(size > 0):
			u = str(isbn.pop())
			k = Details.find({'_id':u})
			if (k.count() == 0):
				get_detail.delay(u)
			print category,size
			size -= 1
                

crawl()
