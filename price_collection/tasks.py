'''
This Module Collect prices from different website
by running celery task worker and store them into
Review collection of dbname databse with timestamp
when price is crawled.
'''
import re
import requests
from pyquery import PyQuery as pq
import datetime
from web_setting import urlset
from celery import Celery

from pymongo import MongoClient


celery = Celery("tasks",
         broker="amqp://guest@localhost")

# connect to mongodb database
connection = MongoClient()
db = connection.dbname
Review = db.Review

# Celery task Implementation for price crawl
@celery.task
def get_review(isbn):
	attrs = {}
	d = {}
	# compile regex for integer matching
	sankhya = re.compile(r'\d+')
	# Tor proxy with port and protocol
	proxy = {'socks4':'127.0.0.1:9050'}
	attrs['_id'] = isbn
	attrs['date'] = datetime.datetime.utcnow()

	''' requests get html content from
	different website and store them in dictionary
	into the memory directly.'''
	for key, value in urlset.items():
		t_url = value + isbn
		key_url = key + '_url'
		attrs[key_url] = t_url
		r = requests.get(t_url, proxies=proxy)
		if r.status_code == 200:
			d[key] = pq(r.text)

	## for Infibeam website Price

	if (d.get('Infibeam') != None):
		Ib = d.get('Infibeam')
		attrs['Infibeam'] = Ib(
                    "span[class=\"infiPrice amount price\"]").text()
	else:
		attrs['Infibeam'] = 'None'


	## for Crossword website Price

	if (d.get('Crossword') != None):
		try:
			attrs['Crossword'] = d.get('Crossword')(
                        "span[class=\"variant-final-price\"]").text().strip('R')
		except AttributeError:
			attrs['Crossword'] = d.get('Crossword')(
                            "span[class=\"variant-final-price\"]").text()
	else:
		attrs['Crossword'] = 'None'


	## for Homeshop18 website Price

	if (d.get('Homeshop18') != None):
		try:
			attrs['Homeshop18'] = d.get('Homeshop18')(
                            "span[id=\"hs18Price\"]").text().split()[1]
		except AttributeError:
			attrs['Homeshop18'] = d.get('Homeshop18')(
                            "span[id=\"hs18Price\"]").text()
	else:
		attrs['Homeshop18'] = 'None'


	## for Bookadda website Price

	if (d.get('Bookadda') != None):
		try:
			attrs['Bookadda'] = d.get('Bookadda')(
                            "span[class=\"actlprc\"]").text().strip('Rs.')
		except AttributeError:
			attrs['Bookadda'] = d.get('Bookadda')(
                            "span[class=\"actlprc\"]").text()

	else:
		attrs['Bookadda'] = 'None'

    ## for rediff book website

	if (d.get('Rediffbook') != None):
		try:
			attrs['Rediffbook'] = d.get('Rediffbook')(
                        "div[class=\"proddetailinforight\"]").text().split()[2]
		except (IndexError, AttributeError), e:
			attrs['Rediffbook'] = d.get('Rediffbook')(
                            "div[class=\"proddetailinforight\"]").text()
	else:
		attrs['Rediffbook'] = 'None'

	# Insert Prices to review Collection
	Review.update({'_id':isbn}, {'$set':{'Rediffbook':attrs['Rediffbook'],
		'Rediffbook_url':attrs['Rediffbook_url'],
		'Infibeam':attrs['Infibeam'],
		'Infibeam_url':attrs['Infibeam_url'],
		'Bookadda':attrs['Bookadda'],
		'Bookadda_url':attrs['Bookadda_url'],
		'Crossword':attrs['Crossword'],
		'Crossword_url':attrs['Crossword_url'],
		'Homeshop18':attrs['Homeshop18'],
		'Homeshop18_url':attrs['Homeshop18_url'],
		'date':attrs['date']}})
