''' 
Before Running this script make sure that you have
already done with the celery tasks for crawl to that
particular category. This script just store the isbn
already crawled to category array in str form. Update 
the category string to run uncomment the last line 
save it then run.
'''

from pymongo import MongoClient
connection = MongoClient()
db = connection.abhi
RISBN = db.RISBN
ISBN= db.ISBN
def list():
	## update this category with crawl.py category
	category = "computers-internet-books-1171" 
	attrs= {}
	isbn = []	
	try:
		cursor = ISBN.find({},{'_id':0})
	except:
        	print "Unexpected error:", sys.docexc_info([0])	
	list = []	
	for d in cursor:
		for t in d.values():
			list.append(t)
	for r in list:
		for k in r:
			h = str(k)			
			isbn.append(h)	
	attrs[category] = isbn
	RISBN.insert(attrs)

