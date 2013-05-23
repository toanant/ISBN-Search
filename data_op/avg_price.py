'''
This module take the input as a json from mongoDB or
simply a result of find_one operation and calculate 
the average price of the book to be used during the
implementation of recommendation algorithm.
'''
import re
from pymongo import MongoClient
con = MongoClient()
abhi = con.abhi
review = abhi.Review


def avg_val(cursor):
    isbn =  cursor.get('_id')
    average = []
    web_list = ['Bookadda', 'Crossword',
         'Homeshop18','Infibeam',
          'Rediffbook', 'flipkart']
    price =  {}

    for site in web_list:
        price[site] = cursor.get(site)

    p = re.compile(r'\d+')

    for k, v in price.items():
        if v == None or v == 'None':
            del price[k]

    for k, v in price.items():
        i = v.replace(',', '')
        price[k] = i

    for k, v in price.items():
        if p.search(v):
            price[k] = int(p.search(v).group())
    for e in price.values():
        average.append(int(e))
    if len(average) > 0:
        average = (min(average) + max(average)) // 2
    review.update({'_id': isbn},
		    {'$set': {'avg_price': average }})

def insert_val():

    cursor = review.find({})
    for e in cursor:
        avg_val(e)

insert_val()

