from pymongo import MongoClient
from pymongo import errors
import json

def db_connect():
	# mlab get connection object to the server space
	#client = MongoClient("ds053176.mlab.com", 53176, connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True)
	try:
		# local
		client = MongoClient()
		# select the database name which you want to work on
		db = client['sistercities']
		db['catergories']
		#db.authenticate("dddm", "sistercities3")
		return db
	except: #pymongo.errors as e
		print("Fail to Authentication.")


def db_insert(collection_name, query):
	# connect to the database
	db = db_connect()
	db[collection_name].insert_one(query)
	print("Successfully Insert")
#	try:
#		#insert the object in the database
#		db[collection_name].insert_one(query)
#		print("Successfully Insert")
#	except:
#		print("Sorry we encountered some error in inserting.")

# unityId is the only parameter on which we query right now. Can be modified to have other parameters as well.
def db_retrieve(collection_name, query):
	db = db_connect()
	try:
		data = db[collection_name].find(query)
		if data.count() == 0:
			print("Not Found: %s" %query)
		for doc in data:
			print("Successfully Retrieved: %s" %doc)
		return data
	except Exception as e:
		print("Sorry we encountered some error in retrieving: %s" %e)


def db_update(collection_name, old, new):
	db = db_connect()
	db[collection_name].update_one(old, new)
#    try:
#		db[collection_name].update_one(old, new) #or update_many
#		print("Update Successful")
#	except:
#		print("Sorry we encountered some error in updating.")

def db_delete(collection_name, query):
	db = db_connect()
	data = db[collection_name].delete_many(query)
	print("Successfully Deleted")
	return data
#	try:
#		data = db[collection_name].delete_many(query)
#		print("Successfully Deleted")
#		return data
#	except Exception as e:
#		print("Sorry we encountered some error in retrieving: %s" %e)