'''
This Crawl script assign task from rabbitMQ Queue to 
celery task to collect price of book from different 
websites.
'''
from tasks import *

def crawl():
    cursor = Review.find({'Bookadda':{'$exists':0}},
		    {'_id':1})
    size = cursor.count()
    i = 0
    while(i < size):
		rev = cursor[i]
		u = str(rev['_id'])
		get_review.delay(u)
		print u
		i += 1

crawl()
