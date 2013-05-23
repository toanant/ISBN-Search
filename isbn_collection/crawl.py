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
	

crawl()                

