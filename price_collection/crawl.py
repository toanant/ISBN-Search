from tasks import *

def crawl():
	size = Review.count()
	i = 0
	while(i < size):
		rev = Review.find()[i]
		u = str(rev['_id'])
		get_review.delay(u)
		print size
		size += 1
                

crawl()
