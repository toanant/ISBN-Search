from tasks import *
def crawl():
	category = 'computers-internet-books-1171'
	start = 0
	isbn  = []
	val = get_data(category,start)
	get_isbn(val['json'], start)
	i = 0
    	while True:
        	i += 1
     		start += 20
	  	print i,start
	    	if (val['count'] != 0):
			val = get_data(category,start)
			get_isbn.delay(val['json'], start)
		else:
			break

crawl()                
