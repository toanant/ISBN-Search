from tasks import *

def crawl():
	cursor = review.find({'Bookadda':{'$exists':0}})
	size = cursor.count()
	i = 0
	while(i < size):
		rev = cursor[i]
		u = str(rev['_id'])
		get_review.delay(u)
		print i
		i += 1
                

crawl()
