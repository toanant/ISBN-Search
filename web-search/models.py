from pymongo import MongoClient

connection = MongoClient()
db = connection.abhi

class BookManager(object):
	def __init__(self):
		## return db.details.find()
		pass

	def paginate(self, start=0, limit=10):
		return db.details.find()

class Book(object):
	objects = BookManager()

	def __init__(self, isbn):
		self.detail = db.details.find_one({"_id": isbn})
		self.review = db.review.find_one({"_id": isbn})

	def __repr__(self):
		return self.name


