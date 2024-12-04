from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import certifi

# MongoDB connection details
DBName = "test"
connectionURL = "mongodb+srv://omaryoussef01:bwSpx7b51aMicKVW@cluster0.7qik9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
virtualTable = "mongoDBtable_virtual"


# Asset UIDs for the devices
fridge_asset_uid = "uz9-9mr-391-mfq"
dishwasher_asset_uid = "2w3-l58-e05-a5c"

def query_database(query_type):
    try:
        # Connect to MongoDB
        client = MongoClient(connectionURL, tlsCAFile=certifi.where())
        db = client[DBName]
        table = db[virtualTable]

        # Define time cutoff for the past 3 hours
        time_cutoff = datetime.now(timezone.utc) - timedelta(hours=3)

        if query_type == "Q1":  # Average moisture in the fridge
            result = table.aggregate([
                {"$match": {"payload.asset_uid": fridge_asset_uid,
                            "time": {"$gte": time_cutoff}}},
                {"$group": {"_id": None,
                            "average_moisture": {"$avg": {"$toDouble": "$payload.Moisture Meter - moistureMeter1"}}}}
            ])
            # Safely return result or fallback
            result_list = list(result)
            return result_list[0]["average_moisture"] if result_list else "No data found for fridge moisture."

        elif query_type == "Q2":  # Average water consumption in the dishwasher
            result = table.aggregate([
                {"$match": {"payload.asset_uid": dishwasher_asset_uid,
                            "time": {"$gte": time_cutoff}}},
                {"$group": {"_id": None,
                            "average_water": {"$avg": {"$toDouble": "$payload.WaterConsumptionSensor"}}}}
            ])
            # Safely return result or fallback
            result_list = list(result)
            return result_list[0]["average_water"] if result_list else "No data found for dishwasher water consumption."

        elif query_type == "Q3":  # Device with the highest electricity consumption
            # Fetch fridge ammeter
            fridge_result = table.aggregate([
                {"$match": {"payload.asset_uid": fridge_asset_uid,
                            "time": {"$gte": time_cutoff}}},
                {"$group": {"_id": None,
                            "total_energy": {"$sum": {"$toDouble": "$payload.Ammeter"}}}}
            ])
            fridge_energy = list(fridge_result)
            fridge_energy_total = fridge_energy[0]["total_energy"] if fridge_energy else 0

            # Fetch dishwasher ammeter
            dishwasher_result = table.aggregate([
                {"$match": {"payload.asset_uid": dishwasher_asset_uid,
                            "time": {"$gte": time_cutoff}}},
                {"$group": {"_id": None,
                            "total_energy": {"$sum": {"$toDouble": "$payload.DishwasherAmmeter"}}}}
            ])
            dishwasher_energy = list(dishwasher_result)
            dishwasher_energy_total = dishwasher_energy[0]["total_energy"] if dishwasher_energy else 0

            # Compare and determine the highest consumer
            if fridge_energy_total > dishwasher_energy_total:
                return f"Fridge ({fridge_asset_uid}) consumed more electricity: {fridge_energy_total:.2f} kWh."
            elif dishwasher_energy_total > fridge_energy_total:
                return f"Dishwasher ({dishwasher_asset_uid}) consumed more electricity: {dishwasher_energy_total:.2f} kWh."
            elif dishwasher_energy_total == fridge_energy_total:
                return "Both devices consumed the same amount of electricity."
            else:
                return "No data found for one or more devices."

        else:
            return "Invalid query type. Please use Q1, Q2, or Q3."

    except Exception as e:
        return f"Database error: {e}"