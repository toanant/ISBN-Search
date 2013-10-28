'''
This Module assign task to celery worker and
store them to RabbitMQ queue for the collection
of details of the book from filpkart website
against the particular isbn and also get price of
that book and store them to Review colection in
MongoDB.
'''
from tasks import *

def crawl():
    isbn =  ISBN.find({'isbn_13':{'$exists':1}}, {'_id':0})
    for e in isbn:
	for h in e.values():
            for t in h:
                var = Details.find_one({'_id':t})
                if (var == None):
                    get_detail.delay(t)
                    print 'got it ', t

if __name__ == '__main__':
    print 'This script will run !!!'
