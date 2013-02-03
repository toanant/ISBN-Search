from flask import Flask, render_template, request
import re
import json
from datetime import datetime
from pymongo import MongoClient
from flask.ext.paginate import Pagination
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
    book = db.details.find_one({"_id": id})
    review = db.review.find_one({"_id": id})
    return render_template("details.html", book=book, review=review)


@app.route("/publisher/<publisher_name>/")
def publisher_page(publisher_name):
    books = db.details.find({"Publisher":
                             re.compile(publisher_name, re.IGNORECASE)})
    return render_template("results.html", books=books)


@app.route("/year/<year>/")
def year_page(year):
    books = db.details.find({"Publication Year":
                             re.compile(year, re.IGNORECASE)})
    return render_template("results.html", books=books)


@app.route("/search/", methods=["GET"])
def search():
    isbn = request.args.get("isbn")
    keywords = request.args.get("keywords")
    start = request.args.get("start")
    limit = request.args.get("limit")
    page = request.args.get("page")
    pattern = re.compile(r"\d{13}")
    if isbn:
        start = 0
        limit = 0
        page = 0
        isbn = pattern.search(isbn).group()
        size = len(isbn)
        if size == 10:
            review = db.review.find({'ISBN-10': isbn})
            isbn = review['_id']
        else:
            review = db.review.find_one({'_id': isbn})

        detail = db.details.find_one({'_id': isbn})

        if detail:
            return render_template("details.html",
                                   book=detail, review=review)
    else:
        books = db.details.find({'keywords':
                                 re.compile(keywords, re.IGNORECASE)})
        return render_template("results.html", books=books)

    return "Query can't be empty."

if __name__ == "__main__":
    app.run(debug=True)
