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
    
    # Fetch all steam games with id and name
    steam_data = requests.get(f"https://api.steampowered.com/ISteamApps/GetAppList/v0001/?key={API_KEY}").json()["applist"]["apps"]["app"]

    # MongoDB contact
    client = MongoClient(mongo_uri)
    db = client["SteamAPI"]
    db_users = db["users"]
    db_games = db["games"]

    # Create games collection using users database
    user_list = db_users.find()
    for user in user_list:
        game_id_list = [int(game_id) for game_id in user["games"]]
        for game_data in steam_data:
            if game_data["appid"] in game_id_list:
                data = {"_id": game_data["appid"], "name": game_data["name"]}
                if db_games.find_one(data):
                    break
                db_games.insert_one(data)



if __name__ == "__main__":
    database_update()