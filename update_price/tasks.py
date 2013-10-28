'''
This will update the review collection against the isbn.
'''
import requests      # Request library for url fetching
from pyquery import PyQuery as pq
from lxml import etree
import datetime
from web_setting import urlset
from celery import Celery

from pymongo import MongoClient

celery = Celery("tasks", broker="amqp://guest@localhost")

# connect to mongodb database
connection = MongoClient()
db = connection.abhi
Review = db.Review

# Initialization of celery task to update price
@celery.task
def update_review(isbn):
    attrs = {}
    d = {}
    # tor proxy with protocol and port address
    proxy = {'socks4':'127.0.0.1:9050'}

    # dump requests from all website into memory
    for key, value in urlset.items():
        t_url = value + isbn
        key_url = key + '_url'
        attrs[key_url] = t_url
        r = requests.get(t_url, proxies=proxy)
        if r.status_code == 200:
            d[key] = pq(r.text)


## Fetch price attribute for flipkart website
    if (d.get('flipkart') != None):
        fk = d.get('flipkart')
        attrs["flipkart"] = fk("meta[itemprop=\"price\"]").attr("content")
        try:
            attrs["ratingValue"] = float(fk
                        ("meta[itemprop=\"ratingValue\"]").attr("content"))
        except (TypeError, ValueError), e:
            attrs["ratingValue"] = 'Not Rated'
        try:
            attrs["ratingCount"] = int(fk
                ("span[itemprop=\"ratingCount\"]").text())
        except (TypeError, ValueError), e:
            attrs["ratingCount"] = 'None'
    else:
        attrs['flipkart'] = 'None'

    # Update time field with current time
    attrs['date'] = datetime.datetime.utcnow()

## Fetch price attribute for Infibeam website Price
    if (d.get('Infibeam') != None):
        Ib = d.get('Infibeam')
        attrs['Infibeam'] = Ib("span[class=\"infiPrice amount price\"]").text()
    else:
        attrs['Infibeam'] = 'None'

## Fetch price attribute for Crossword website Price
    if (d.get('Crossword') != None):
        try:
            attrs['Crossword'] = d.get('Crossword')(
                "span[class=\"variant-final-price\"]").text().strip('R')
        except AttributeError:
            attrs['Crossword'] = d.get('Crossword')(
                            "span[class=\"variant-final-price\"]").text()
    else:
        attrs['Crossword']      = 'None'

## Fetch price attribute for Homeshop18 website Price
    if (d.get('Homeshop18') != None):
        try:
            attrs['Homeshop18'] = d.get('Homeshop18')(
                            "span[id=\"hs18Price\"]").text().split()[1]
        except AttributeError:
            attrs['Homeshop18'] = d.get('Homeshop18')(
                            "span[id=\"hs18Price\"]").text()
    else:
        attrs['Homeshop18'] = 'None'

## Fetch price attribute for Bookadda website Price
    if (d.get('Bookadda') != None):
        try:
            attrs['Bookadda'] = d.get('Bookadda')(
                            "span[class=\"actlprc\"]").text().strip('Rs.')
        except AttributeError:
            attrs['Bookadda'] = d.get('Bookadda')(
                            "span[class=\"actlprc\"]").text()

    else:
        attrs['Bookadda'] = 'None'
##Fetch price attribute for rediff book website
    if (d.get('Rediffbook') != None):
        try:
            attrs['Rediffbook'] = d.get('Rediffbook')(
                        "div[class=\"proddetailinforight\"]").text().split()[2]
        except (IndexError, AttributeError), e:
            attrs['Rediffbook'] = d.get('Rediffbook')(
                            "div[class=\"proddetailinforight\"]").text()
    else:
        attrs['Rediffbook'] = 'None'

        # Update the review Collection Object's price for particular isbn
    Review.update({'_id': isbn}, {'$set': {'Rediffbook':
            attrs['Rediffbook'], 'Infibeam': attrs['Infibeam'],
            'Bookadda': attrs['Bookadda'], 'Crossword': attrs['Crossword'],
            'Homeshop18':attrs['Homeshop18'], 'date': attrs['date'],
            'ratingCount': attrs.get('ratingCount'),
                'ratingValue': attrs.get('ratingValue')}})

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
