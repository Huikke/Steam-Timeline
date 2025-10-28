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
    db_activity = db["activity"]

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
        game_list[str(appid)] = {"playtime": playtime, "last_time_played": last_time_played}

    # Compare with database
    # If user does not exist, create it
    if db_users.find_one(user_id) == None:
        print("user not found, adding")
        db_users.insert_one({"_id": user_id, "games": game_list})
        # For previous played time keeping purposes
        db["users_legacy"].insert_one({"_id": user_id}, {"$set": {"games": game_list}})

    # Get the user's game list from database
    fetched_game_list = db_users.find_one(user_id)["games"]
    # Check if the current game list matches the database
    if game_list == fetched_game_list:
        print("they're the same!")
    else:
        # Iterate through each game in current list to find changes
        for game in game_list:
            if game_list[game] != fetched_game_list.get(game):
                # Set previous playtime to 0 if game is new, otherwise get from database
                if fetched_game_list.get(game) == None:
                    playtime_fetched = 0
                else:
                    playtime_fetched = fetched_game_list[game]["playtime"]

                # Get current game stats
                playtime_now = game_list[game]["playtime"]
                last_time_played_now = game_list[game]["last_time_played"]
                # Get current timestamp in ISO format
                timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

                # Create activity record with changes
                activity = { "timestamp": timestamp, "user": user_id, "game": game,
                            "prev_playtime": playtime_fetched, "current_playtime": playtime_now, "last_played": last_time_played_now}
                # Insert activity record into database
                db_activity.insert_one(activity)
                print(game,"changed")
        # Update user's game list in database
        db_users.update_one({"_id": user_id}, {"$set": {"games": game_list}})



if __name__ == "__main__":
    database_update()