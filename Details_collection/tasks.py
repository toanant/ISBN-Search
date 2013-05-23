'''
This module collect details & price of book from flipkart website 
against the isbn using celery worker task assigned by RabbitMQ 
broker.
'''
from pymongo import MongoClient
import requests

import datetime
from pyquery import PyQuery as pq
from lxml import etree
from celery import Celery

celery = Celery("tasks", broker="amqp://guest@localhost")

# mongodb connection with db as abhi
connection = MongoClient()
db = connection.abhi
ISBN = db.ISBN
Details = db.Details
Review = db.Review

# Implementation of task to get details and price
@celery.task
def get_detail(val):
	detail = {}
	proxy = {'socks4':'127.0.0.1:9050'}
	attrs = {}
    ## fk represent attributes for review collection
	fk = {}
	base_url = 'http://www.flipkart.com/search.php?query='
	url = base_url + val
##view_text_url = 'http://viewtext.org/api/text?url=%s&format=json'%(url)
	r = requests.get(url, proxies=proxy)
	if r.status_code == 200:
       ## vt = request.get(view_text_url)

		d = pq(r.text)
		summary =  d('div[id="description"]').html()
		if(summary != None):
			attrs['summary'] = summary
		else:
			attrs['summary'] = None
		fk["flipkart"] = d("meta[itemprop=
					\"price\"]").attr("content")
		try:
			fk["ratingValue"] = float(d("meta[itemprop=
				\"ratingValue\"]").attr("content"))
		except (TypeError, ValueError), e:
			fk["ratingValue"] = 'Not Rated'
		try:
			fk["ratingCount"] = int(d("span[itemprop=
					\"ratingCount\"]").text())
		except (TypeError, ValueError), e:
			fk["ratingCount"] = 'None'
		fk['_id'] = val
		fk['flipkart_url'] = url
		if(d("#mprodimg-id").find("img").attr("data-src") != None):
			attrs['image'] = d("#mprodimg-id").find("img").attr("data-src")
		else:
			attrs['image'] = d('.image-wrapper > img').attr('src')

		attrs["name"] = d("h1[itemprop=
					\"name\"]").attr("title")
		if( d(".secondary-info > a").text()):
			attrs["author"] = d(".secondary-info > a").text()
		else:
			try:
				attrs['author'] = d('.secondary-info').text().split('Publisher')[0].split(':')[1]
			except (IndexError, AttributeError), e:
				attrs['author'] = 'None'
		attrs["keywords"] =  d("meta[name=
					\"Keywords\"]").attr("content").split(",")
		td_set = d(".fk-specs-type2 > tr >td").items()
		for key in td_set:
			detail[key.text()] = td_set.next().text()

		attrs['Publisher'] = detail.get('Publisher')
		attrs['Publication Year']= detail.get('Publication Year')
		attrs['_id'] = val
		attrs['ISBN-10'] = detail.get('ISBN-10')
		attrs['Language'] = detail.get('Language')
		attrs['Binding'] = detail.get('Binding')
		attrs['Number of Pages'] = detail.get('Number of Pages')
		attrs['date'] = datetime.datetime.utcnow()

		# Insert Details and Price to Database 
		Details.insert(attrs)
		Review.insert(fk)
