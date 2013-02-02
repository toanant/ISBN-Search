import requests
from pyquery import PyQuery as pq
from lxml import etree

from web_setting import *
from celery import Celery

from pymongo import MongoClient

#from pyelasticsearch import ElasticSearch

celery = Celery("tasks", broker="amqp://guest@localhost")

# connect to mongodb database
connection = MongoClient()
db = connection.abhi
# Here RISBN define refined isbn collection in a list associated with category
ISBN= db.ISBN
@celery.task
def get_isbn(category):
	attrs = {}
	isbn = []
	start = 0
	while(True):
		url = 'http://www.flipkart.com/%s?response-type=json&inf-start=%d'%(category, start)
		r = requests.get(url)
		if r.status_code == 200:
			json= r.json()
			count = json['count']
			if(count ==0):
				break
			d = pq(json["html"])
			# here p contains all the <a href with div class = "">
			p = d("div[class=\"lastUnit rposition\"] a")
			for e in p:
				t = (str(e.values())).strip("]").split("pid=")
				if(len(t)==2):
					isbn.append((t[1])[:13])
		
		else:
			print category, start
			break
		start += 20
	attrs[category]	= isbn	
	
	ISBN.insert(attrs)	
