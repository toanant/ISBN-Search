from tasks import *
from datetime import timedelta

def crawl():
	i = Review.count()
	while(i >= 0):
		result = Review.find()[i-1]
		u = str(result['_id'])
		past = result['date']
		now = datetime.datetime.utcnow()
		if ((now - past) > timedelta(hours = 84)):
			update_review.delay(u)
		
		print i
		i -= 1
                

crawl()

