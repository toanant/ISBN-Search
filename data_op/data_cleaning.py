'''
This module take the input as a json from mongoDB or
simply a result of find_one operation and clean the
content from unwanted symbols, strings and encode
them into utf-8 and update into database.
'''
import re
#import operator
from pymongo import MongoClient
con = MongoClient()
dbname = con.dbname
review = dbname.Review
detail  = dbname.Details

def clean_val(cursor):
    isbn =  cursor.get('_id')


    year = cursor.get('Publication Year')
    if year == None:
        year = 'None'
    year = year.encode('utf-8', 'ignore')
    year = str(year)

    year = year.replace('/', '-')
    publisher = cursor.get('Publisher')
    if publisher == None:
        publisher = 'general'
    publisher = publisher.encode("utf-8", 'ignore')
    publisher = str(publisher)
    publisher = publisher.replace('/', ' ')
    publisher = publisher.replace('(', '')
    publisher = publisher.replace(')', '')
    publisher = publisher.replace('?', ' ')
    publisher = publisher.replace('\\', ' ')


    name = cursor.get('name')
    if name == None:
        name = 'general'
    name = name.encode('utf-8', 'ignore')
    name = str(name)
    name.replace('?', '')


    author = cursor.get('author')
    if author == 'None':
        author = 'general'
    author = author.encode('utf-8', 'ignore')
    author = str(author)
    author = author.replace('?', '')
    author = author.replace('*', '')
    author = author.replace('[', '')
    author = author.replace('(', '')
    author = author.replace(')', '')
    detail.update({'_id': isbn},
        {'$set': {'Publication Year': year, 'Publisher': publisher,
                  'name': name, 'author': author }})

def update_val():

    cursor = detail.find({})
    for e in cursor:
        clean_val(e)

if __name__ == '__main__':
    update_val()

