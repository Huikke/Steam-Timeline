import os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
from datetime import datetime

# Fetches from Steam API, make changes to it, and upload it to MongoDB (WIP)
def activity_fetcher():
    # Set .env variables
    mongo_uri = os.getenv("mongo_uri")
    if mongo_uri == None:
        raise Exception(".env lacks necessary components")

    # MongoDB contact
    client = MongoClient(mongo_uri)
    db = client["SteamAPI"]
    db_users = db["users"]
    db_activity = db["activity"]

    # Fetcher itself
    activities = db_activity.find()
    fetched_list = []
    for activity in activities:
        timestamp = activity["timestamp"].replace("T", " ").split("+")[0]
        last_played = datetime.fromtimestamp(activity["last_played"])
        fetched_list.append((timestamp, activity["game"], activity["prev_playtime"], activity["current_playtime"], last_played))

    return fetched_list


if __name__ == "__main__":
    fetched = activity_fetcher()
    print(fetched)