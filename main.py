import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient

# Fetches from Steam API, make changes to it, and upload it to MongoDB (WIP)
def database_update():
    # Set .env variables
    API_KEY = os.getenv("steam_api_key")
    user_id = os.getenv("steam_id")
    mongo_uri = os.getenv("mongo_uri")
    if API_KEY == None or user_id == None or mongo_uri == None:
        raise Exception(".env lacks necessary components")

    # MongoDB contact
    client = MongoClient(mongo_uri)
    db = client["SteamAPI"]
    db_users = db["users"]
    db_games = db["games"]

    # Get owned games data from Steam API
    response = requests.get(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={user_id}")
    data_new = response.json()["response"]["games"]

    # Put games into dictionary
    game_list = {}
    for game in data_new:
        # Don't upload games that have not been played
        if game["playtime_forever"] == 0:
            continue
        
        # Helper variables
        appid = game["appid"]
        playtime = game["playtime_forever"]
        last_time_played = game["rtime_last_played"]

        # Add to local dict
        game_list[str(appid)] = [playtime, last_time_played]

    # Upload to MongoDB
    user_info = {"_id": user_id, "games": game_list}
    db_users.insert_one(user_info)



if __name__ == "__main__":
    database_update()