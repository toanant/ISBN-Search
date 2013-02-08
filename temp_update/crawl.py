from tasks import *
def crawl():
	size = 1927
	k = 0 
	while(k < size):
		detail = details.find()[k]
		if (detail.get('image') == None):
			u = detail.get('_id') 
			get_detail.delay(u)
			print k,size
		k += 1
                    

crawl()
