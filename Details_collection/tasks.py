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
    view_text_url = 'http://viewtext.org/api/text?url=%s&format=json'%(url)
    r = requests.get(url)
    if r.status_code == 200:
        vt = request.get(view_text_url)
        attrs['summary'] = vt.json()["content"].decode("unicode_escape")
              
        d = pq(r.text)
        fk["flipkart"] = d("meta[itemprop=\"price\"]").attr("content")
        try:
            fk["ratingValue"] = float(d("meta[itemprop=\"ratingValue\"]").attr("content"))
        except (TypeError, ValueError), e:
            fk["ratingValue"] = 'Not Rated'
        try:
                fk["ratingCount"] = int(d("span[itemprop=\"ratingCount\"]").text())
        except (TypeError, ValueError), e:
                fk["ratingCount"] = 'None'
        fk['_id'] = val
        fk['flipkart_url'] = url
        attrs['image'] = d("#mprodimg-id").find("img").attr("data-src")
        attrs["name"] = d("h1[itemprop=\"name\"]").attr("title")
        attrs["author"] = d(".secondary-info > a").text()
        attrs["keywords"] =  d("meta[name=\"Keywords\"]").attr("content").split(",")
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
        Details.insert(attrs)
        Review.insert(fk)
        
