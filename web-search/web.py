from flask import Flask, render_template, request
import re
import json
from datetime import datetime
from pymongo import MongoClient
from flask.ext.paginate import Pagination
from check_isbn import *
# from pyelasticsearch import ElasticSearch


# connect to mongodb database
connection = MongoClient()
db = connection.abhi

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/books/<id>/")
def detail(id):
    book = db.Details.find_one({"_id": id})
    review = db.Review.find_one({"_id": id})
    return render_template("details.html", book=book, review=review)


@app.route("/author/<author_name>/")
def author_page(author_name):
    books = db.Details.find({"author":
                             re.compile(author_name, re.IGNORECASE)})
    return render_template("results.html", books=books)

@app.route("/publisher/<publisher_name>/")
def publisher_page(publisher_name):
	publisher_name = str(publisher_name)
	publisher_name = publisher_name.replace('/',' ')
	books = db.Details.find({"Publisher":
                             re.compile(publisher_name, re.IGNORECASE)})
	return render_template("results.html", books=books)


@app.route("/year/<year>/")
def year_page(year):
    books = db.Details.find({"Publication Year":
                             re.compile(year, re.IGNORECASE)})
    return render_template("results.html", books=books)


@app.route("/search/", methods=["GET"])
def search():
	isbn = request.args.get("isbn")
	keywords = request.args.get("keywords")
	pattern_13 = re.compile(r"\d{13}")
	_started_at = datetime.now()
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
			return render_template("details.html",
                                   book=detail, review=review)
		else: 
			return render_template("Error.html")
	elif keywords:
		if len(keywords) == 0:
			return render_template("Error.html")
		else:
			books = db.Details.find({'keywords':re.compile(keywords, re.IGNORECASE)})
			if (books.count() != 0):
				return render_template("results.html",books=books)
			else:
				return render_template("Error.html")
	else:
		return " You must enter the query"
if __name__ == "__main__":
	app.run(debug=True)

