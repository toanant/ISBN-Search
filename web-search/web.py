'''
This web.py script is implemented using Flask in collaboration
with pymongo to interact with MongoDB. This Script simply work 
as a web framework & renders the HTML pages defined in 
Templates with dynamic content.
'''
 # import of flask & its component 
from flask import Flask, render_template,request

# import of regular expression from standard library
import re  

# import of json module from python's standard library
import json 
from datetime import datetime, timedelta 

# MongoDB native drive for python
from pymongo import MongoClient 
from flask.ext.paginate import Pagination

# Sort prices dynamically in increasing order
from price_sort import * 

# script to check valid isbn
from check_isbn import * 

 # Script for recommendation algorithm 
from recommendation import *


# connect to mongodb database
connection = MongoClient()
db = connection.abhi

# defining Flask application here 
app = Flask(__name__)


# Home url implementation  
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/robots.txt")
def robots():
    return render_template("robots.txt")

# Book details page url with isbn implementation
@app.route("/books/<id>/")
def detail(id):
    book = db.Details.find_one({"_id": id})
    review = db.Review.find_one({"_id": id})
    book_prices = sort_prices(review)
    recn = suggest_book(book, review)
    return render_template("details.html", 
            book=book, prices=book_prices,
		    review=review, recn=recn)

# search implementation for isbn and keyword separately
@app.route("/search/", methods=["GET"])
def search():

    # get isbn from search field
    isbn = request.args.get("isbn") 
    
    # get the keywords
    keywords = request.args.get("keywords", "").strip() 

    if not isbn and len(keywords) < 2:
            return render_template("Error.html")

    # compile to get 13 digit isbn 
    pattern_13 = re.compile(r"\d{13}") 
    if isbn:
        if pattern_13.search(isbn):
            isbn = pattern_13.search(isbn).group()
            if(is_isbn13(isbn)):
                isbn = isbn
            else:
                return render_template('Error.html')
        else:
            if(is_isbn10(isbn)):
                isbn = isbn
            else:
                return render_template('Error.html')
        size = len(isbn)
        if size == 10:
            detail = db.Details.find_one({'ISBN-10':isbn})
            isbn = detail.get('_id')
        else:
            detail = db.Details.find_one({'_id': isbn})
        review = db.Review.find_one({'_id': isbn})
        if detail:
            book_prices = sort_prices(review)
            return render_template("details.html",
                         book=detail,
			            review=review, prices=book_prices)
        else:
            return render_template("Error.html")
    elif keywords:
        if len(keywords) == 0:
            return render_template("Error.html")
        else:

            books = db.Details.find({'keywords':
                            re.compile(keywords,
		                re.IGNORECASE)}).limit(37)
            if (books.count() != 0):
                return render_template("results.html",
                                books=books)
            else:
                return render_template("Error.html")
    else:
        return render_template("Error.html")
# run the application with debug as True 
if __name__ == "__main__":
    app.run(debug=True)

