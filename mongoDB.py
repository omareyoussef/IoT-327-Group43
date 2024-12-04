from pymongo import MongoClient, database
import subprocess
import threading
import pymongo
from datetime import datetime, timedelta,timezone
import time
import certifi

DBName = "test" 
connectionURL = "mongodb+srv://jeffkim:lWRrXOkPvEjzvO3Z@2024fall327.aemto.mongodb.net/?retryWrites=true&w=majority&appName=2024Fall327" 
virtualTable = "mongo_virtual" 

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

		#We first ask the user which collection they'd like to draw from.
		virtualTableObject = db[virtualTable]

		#We convert the cursor that mongo gives us to a list for easier iteration.
		# Convert the time now in the current location to UTC, then subtract 180 minutes to get all the documents generated 
		# in the past 3hours
		timeCutOff = datetime.now(timezone.utc) - timedelta(minutes=180)
		timeQuery = virtualTableObject.find({"time":{"$gte":timeCutOff}})
		currentDocuments = QueryToList(timeQuery)
		return currentDocuments
		
    #if connection is not built or couldnt retrieve any data, runs exception.
	except Exception as e:
		print("Please make sure that this machine's IP has access to MongoDB.")
		print("Error:",e)
		exit(0)
	
