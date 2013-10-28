'''
This Module will crawl flipkart website and get
json output containing isbn for different category.
Start this by running celery task worker in the
activated virtualenvironment.
'''
import requests
from pyquery import PyQuery as pq

from web_setting import urlset
from celery import Celery

from pymongo import MongoClient


celery = Celery("tasks", broker="amqp://guest@localhost")

# connect to mongodb database
connection = MongoClient()
db = connection.abhi
# ISBN define isbn collection in a list associated with category
ISBN = db.ISBN

@celery.task
def get_isbn(category):
    attrs = {}
    isbn = []
    start = 0
    while(True):
        # category and start get json for that page on flipkart
        url = 'http://www.flipkart.com/%s?response-type=json&inf-start=%d' %(
            category,start)
        r = requests.get(url)
        if r.status_code == 200:
            json = r.json()
            count = json['count']
            if(count ==0):
                break
            d = pq(json["html"]
            p = d("div[class=\"lastUnit rposition\"] a")
            for e in p:
                t = (str(e.values())).strip("]").split("pid=")
                if(len(t)==2):
                    isbn.append((t[1])[:13])

	else:
            print category, start
            break
        start += 20
    attrs[category] = isbn

    ISBN.insert(attrs)
