from pymongo import MongoClient, database
import subprocess
import threading
import pymongo
from datetime import datetime, timedelta,timezone
import time
import certifi

DBName = "test" 
connectionURL = "mongodb+srv://jeffkim:lWRrXOkPvEjzvO3Z@2024fall327.aemto.mongodb.net/?retryWrites=true&w=majority&appName=2024Fall327" 
virtualTable = "table_virtual" 
ids = {"zwl-0y3-7ob-93e", "c84d3021-5582-402e-b3ae-2118ff775916","bb113181-961a-43ed-9f35-2a2c9dd74616"}

def QueryToList(query):
	# Iterate through the query and put it in a list.
	queryList = []
	for doc in query:
		queryList.append(doc)
	return queryList

def QueryDatabase() -> list[dict]:
	global DBName
	global connectionURL
	global currentDBName
	global running
	global filterTime
	global virtualTable
	cluster = None
	client = None
	db = None
	try:
		cluster = connectionURL
		client = MongoClient(connectionURL, tlsCAFile=certifi.where())
		db = client[DBName]
		print("Database collections: ", db.list_collection_names())

		#We first ask the user which collection they'd like to draw from.
		virtualTableObject = db[virtualTable]
		print("Table:", virtualTableObject)

		#We convert the cursor that mongo gives us to a list for easier iteration.
		# Convert the time now in the current location to UTC, then subtract 5 minutes to get all the documents generated 
		# in the past 5 minutes.
		timeCutOff = datetime.now(timezone.utc) - timedelta(minutes=10800)
		timeQuery = virtualTableObject.find({"time":{"$gte":timeCutOff},"payload.parent_asset_uid": {"$in": list(ids)}})
		# idQuery = timeQuery.find({"parent_asset_uid": {"$in": ids}})
		currentDocuments = QueryToList(timeQuery)
		return currentDocuments
		


	except Exception as e:
		print("Please make sure that this machine's IP has access to MongoDB.")
		print("Error:",e)
		exit(0)
		
print(QueryDatabase())