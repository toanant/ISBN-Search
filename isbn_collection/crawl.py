from tasks import *
def crawl():
	for category in CATEGORIES:
		print category
		get_isbn.delay(category)
	

crawl()                

