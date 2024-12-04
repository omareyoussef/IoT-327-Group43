from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import certifi

# MongoDB connection details
DBName = "test"
connectionURL = "mongodb+srv://omaryoussef01:bwSpx7b51aMicKVW@cluster0.7qik9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
virtualTable = "table_virtual"

def query_database(query_type):
    try:
        client = MongoClient(connectionURL, tlsCAFile=certifi.where())
        db = client[DBName]
        table = db[virtualTable]

        # Define time cutoff for the past 3 hours
        time_cutoff = datetime.now(timezone.utc) - timedelta(hours=3)

        if query_type == "Q1":  # Average moisture in the kitchen fridge
            result = table.aggregate([
                {"$match": {"device_type": "fridge", "time": {"$gte": time_cutoff}}},
                {"$group": {"_id": None, "average_moisture": {"$avg": "$payload.moisture"}}}
            ])
            return list(result)[0]["average_moisture"] if result else "No data found"

        elif query_type == "Q2":  # Average water consumption in the dishwasher
            result = table.aggregate([
                {"$match": {"device_type": "dishwasher", "time": {"$gte": time_cutoff}}},
                {"$group": {"_id": None, "average_water": {"$avg": "$payload.water_usage"}}}
            ])
            return list(result)[0]["average_water"] if result else "No data found"

        elif query_type == "Q3":  # Device with highest electricity consumption
            result = table.aggregate([
                {"$match": {"device_type": {"$in": ["fridge", "dishwasher"]}, "time": {"$gte": time_cutoff}}},
                {"$group": {"_id": "$device_id", "total_energy": {"$sum": "$payload.energy_usage"}}},
                {"$sort": {"total_energy": -1}},
                {"$limit": 1}
            ])
            return list(result)[0]["_id"] if result else "No data found"

    except Exception as e:
        return f"Database error: {e}"