from pymongo import MongoClient
import requests

import datetime
#from web_setting import *
from pyquery import PyQuery as pq
from lxml import etree
from celery import Celery

celery = Celery("tasks", broker="amqp://guest@localhost")

# mongodb connection with db as abhi
connection = MongoClient()
db = connection.abhi
details = db.details
#Review = db.Review
@celery.task
def get_detail(val):
	attrs = {}
	base_url = 'http://www.flipkart.com/search.php?query='
	url = base_url + val
	view_text_url = 'http://viewtext.org/api/text?url=%s&format=json'%(url)
	r = requests.get(url)
	if r.status_code == 200:
		vt = requests.get(view_text_url)
		try:
			attrs['summary'] = vt.json()["content"].decode("unicode_escape")
		except AttributeError:
			attrs['summary'] = 'Not available'
		d = pq(r.text)
		if(d("#mprodimg-id").find("img").attr("data-src") != None):
			attrs['image'] = d("#mprodimg-id").find("img").attr("data-src")
		else:
			attrs['image'] = d('.image-wrapper > img').attr('src')
		attrs["author"] = d(".secondary-info > a").text()
		details.update({'_id':val},{'$set':{'summary':attrs.get('summary'), 'image':attrs.get('image'), 'author':attrs.get('author')}})

