import requests
import json
from datetime import datetime
import time

url = "urlhere"
seen_messages = set()

def ping_server():
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        return data
    except Exception as e:
        print("Error:", e)
        return None

def extract_chat_messages(data):
    global seen_messages
    if data and "updates" in data:
        with open("chat_log.txt", "a") as file:
            for item in data["updates"]:
                if "type" in item:
                    message_type = item["type"]
                    if message_type == "chat" and "source" in item and item["source"] == "player":
                        message_key = (item.get('timestamp'), item.get('account'), item.get('message'))
                        if message_key not in seen_messages:
                            timestamp = datetime.now().strftime("%y/%m/%d/%H:%M:%S")
                            message = f"<{item.get('account')}> {item.get('message')} [{timestamp}]\n"
                            file.write(message)
                            seen_messages.add(message_key)
                    elif message_type == "playerquit":
                        quit_key = (item.get('timestamp'), item.get('account'))
                        if quit_key not in seen_messages:
                            timestamp = datetime.now().strftime("%y/%m/%d/%H:%M:%S")
                            message = f"{item.get('account')} left the game [{timestamp}]\n"
                            file.write(message)
                            seen_messages.add(quit_key)
                    elif message_type == "playerjoin":
                        join_key = (item.get('timestamp'), item.get('account'))
                        if join_key not in seen_messages:
                            timestamp = datetime.now().strftime("%y/%m/%d/%H:%M:%S")
                            message = f"{item.get('account')} joined the game [{timestamp}]\n"
                            file.write(message)
                            seen_messages.add(join_key)

def main():
    while True:
        data = ping_server()
        extract_chat_messages(data)
        # Add a delay between each update (optional)
        time.sleep(1)

if __name__ == "__main__":
    main()
