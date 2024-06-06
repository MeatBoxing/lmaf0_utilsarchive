import requests
import json
import os
import datetime
import time

# Function to fetch player data and save to JSON files
def fetch_and_append_player_data(url, save_folder):
    while True:
        try:
            # Make a GET request to the provided URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Convert response content to JSON format
                data = response.json()

                # Extract players data
                players = data.get("players", [])

                # Get current timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                # Loop through each player
                for player in players:
                    # Generate filename based on account name
                    filename = os.path.join(save_folder, f"{player['account']}.json")

                    # Ensure the directory exists
                    os.makedirs(save_folder, exist_ok=True)

                    # Check if the file already exists
                    if os.path.exists(filename):
                        # Read existing data from the file
                        with open(filename, "r") as f:
                            existing_data = json.load(f)
                    else:
                        # Create a new file if it doesn't exist
                        existing_data = []

                    # Append new player data to existing data
                    existing_data.append({
                        "timestamp": timestamp,
                        "account": player["account"],
                        "x": player["x"],
                        "y": player["y"],
                        "z": player["z"],
                        "health": player["health"],
                        "armor": player["armor"],
                        "world": player["world"]
                    })

                    # Save updated data to the file
                    with open(filename, "w") as f:
                        json.dump(existing_data, f, indent=4)

                    print(f"Appended player data for {player['account']} to {filename}")

            else:
                print("Failed to fetch player data")

        except Exception as e:
            # Ignore all errors
            pass

        # change interval to ping server. in seconds
        time.sleep(5)

# URL to fetch player data
url = "urlhere"

# Folder to save JSON files
save_folder = "users"

# Call the function to fetch and append player data
fetch_and_append_player_data(url, save_folder)
