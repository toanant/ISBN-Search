'''
This Crawl module assign task from RabbitMQ
Queue to celery worker task to collect isbn from
different category of books on flipkart website.
'''
from tasks import *
def crawl():
	for category in CATEGORIES:
		print category
		get_isbn.delay(category)

if __name__ == '__main__':
    print 'This program is being run by itself'

