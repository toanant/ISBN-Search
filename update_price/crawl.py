'''
This Script work with celery and assign task to update
Prices of Books whose price are older than 72 hours.
'''

from tasks import *
from datetime import timedelta

def crawl():
    i = Review.count()
    while(i >= 0):
        result = Review.find()[i-1]
        u = str(result['_id'])
        past = result['date']
        now = datetime.datetime.utcnow()
        if ((now - past) > timedelta(hours = 72)):
            update_review.delay(u)
            print u
        print i
        i -= 1

if __name__ == '__main__':
    crawl()

