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
second_fridge_asset_uid = "c15f2c3d-8d22-4d96-8b26-495a2853fbf0"

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
                            "average_moisture": {"$avg": {"$toDouble": "$payload.MoistureMeter1"}}}}
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
            # Fetch fridge 1 ammeter
            fridge1_result = table.aggregate([
                {"$match": {"payload.asset_uid": fridge_asset_uid,
                            "time": {"$gte": time_cutoff}}},
                {"$group": {"_id": None,
                            "total_energy": {"$sum": {"$toDouble": "$payload.Fridge1Ammeter"}}}}
            ])
            fridge1_energy = list(fridge1_result)
            fridge1_energy_total = fridge1_energy[0]["total_energy"] if fridge1_energy else 0

            # Fetch fridge 2 ammeter
            fridge2_result = table.aggregate([
                {"$match": {"payload.asset_uid": second_fridge_asset_uid,
                            "time": {"$gte": time_cutoff}}},
                {"$group": {"_id": None,
                            "total_energy": {"$sum": {"$toDouble": "$payload.Fridge2Ammeter"}}}}
            ])
            fridge2_energy = list(fridge2_result)
            fridge2_energy_total = fridge2_energy[0]["total_energy"] if fridge2_energy else 0

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
            if fridge1_energy_total > fridge2_energy_total and fridge1_energy_total > dishwasher_energy_total:
                return f"Fridge 1 ({fridge_asset_uid}) consumed more electricity: {fridge1_energy_total:.2f} kWh."
            elif fridge2_energy_total > fridge1_energy_total and fridge2_energy_total > dishwasher_energy_total:
                return f"Fridge 2 ({second_fridge_asset_uid}) consumed more electricity: {fridge2_energy_total:.2f} kWh."
            elif dishwasher_energy_total > fridge1_energy_total and dishwasher_energy_total > fridge2_energy_total:
                return f"Dishwasher ({dishwasher_asset_uid}) consumed more electricity: {dishwasher_energy_total:.2f} kWh."
            elif fridge1_energy_total == fridge2_energy_total and fridge1_energy_total > dishwasher_energy_total:
                return f"Fridge 1 and Fridge 2 consumed the same highest electricity: {fridge1_energy_total:.2f} kWh."
            elif fridge1_energy_total == dishwasher_energy_total and fridge1_energy_total > fridge2_energy_total:
                return f"Fridge 1 and Dishwasher consumed the same highest electricity: {fridge1_energy_total:.2f} kWh."
            elif fridge2_energy_total == dishwasher_energy_total and fridge2_energy_total > fridge1_energy_total:
                return f"Fridge 2 and Dishwasher consumed the same highest electricity: {fridge2_energy_total:.2f} kWh."
            elif fridge1_energy_total == fridge2_energy_total == dishwasher_energy_total and dishwasher_energy_total != 0.0:
                return f"All three devices consumed the same electricity: {fridge1_energy_total:.2f} kWh."
            else:
                return "No data found for one or more devices."

        else:
            return "Invalid query type. Please use Q1, Q2, or Q3."

    except Exception as e:
        return f"Database error: {e}"