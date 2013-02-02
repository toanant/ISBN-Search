from pymongo import MongoClient
import requests
import datetime
from web_setting import *
from pyquery import PyQuery as pq
from lxml import etree
from celery import Celery

celery = Celery("tasks", broker="amqp://guest@localhost")

# mongodb connection with db as abhi
connection = MongoClient()
db = connection.abhi
RISBN = db.RISBN
Details = db.Details
Review = db.Review
@celery.task
def get_detail(val):
	detail = {}	
	l = []
    attrs = {}
	## fk represent attributes related to flipkart review collection
	fk = {}
	base_url = 'http://www.flipkart.com/search.php?query='
	url = base_url + val
	r = requests.get(url)
	if r.status_code == 200:
		d = pq(r.text)
		fk["flipkart"] = d("meta[itemprop=\"price\"]").attr("content")
		try:
			fk["ratingValue"] = float(d("meta[itemprop=\"ratingValue\"]").attr("content"))
		except TypeError:
			fk["ratingValue"] = 'Not Rated'
		try:
				fk["ratingCount"] = int(d("span[itemprop=\"ratingCount\"]").text())
		except TypeError:
				fk["ratingCount"] = 'None'
		fk['_id'] = val
		fk['flipkart_url'] = url

		attrs["name"] = d("h1[itemprop=\"name\"]").attr("title")
        attrs["keywords"] =  d("meta[name=\"Keywords\"]").attr("content").split(",")
		table = d(".fk-specs-type2")
		for t in table.children():
			l.append(t.text_content().strip().splitlines())
		i = 1
     		b = len(l)
    		while(i < b):
			try:
				detail[l[i][0]] = l[i][1].strip()
				i +=1
			except IndexError:
				i = b +1

		attrs['Publisher'] = detail.get('Publisher')
		attrs['Publication Year']= detail.get('Publication Year')
		attrs['_id'] = val
		attrs['ISBN-10'] = detail.get('ISBN-10')
		attrs['Language'] = detail.get('Language')
		attrs['Binding'] = detail.get('Binding')
		attrs['Number of Pages'] = detail.get('Number of Pages')
		attrs['date'] = datetime.datetime.utcnow()
		Details.insert(attrs)
		Review.insert(fk)
		
