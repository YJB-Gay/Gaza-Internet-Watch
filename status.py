import os
import json
import requests
import time
from collections import Counter
from datetime import datetime, timedelta

current_unix_timestamp = int(time.time())

script_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(script_directory)
config_file_path = os.path.join(parent_directory, 'config.json')
with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)

discord_webhook_url = config["discord"]["webhook_url"]
openweather_api_key = config["openweather"]["api_key"]

# Read data from cache.json
with open('cache.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
json_url = data["json_url"]
# Define the folder where the JSON files are located
log_folder = "logs"
# List all JSON files in the folder
json_files = [f for f in os.listdir(log_folder) if f.endswith(".json")]
png_files = [f for f in os.listdir(log_folder) if f.endswith(".png")]

# Sort the files by modification time and get the most recent one
most_recent_png = max(png_files, key=lambda f: os.path.getmtime(os.path.join(log_folder, f)))
most_recent_json = max(json_files, key=lambda f: os.path.getmtime(os.path.join(log_folder, f)))

# Read the most recent JSON file
with open(os.path.join(log_folder, most_recent_json), 'r') as file:
    data = json.load(file)

# Extract the 'status' field from each entry in 'ip_status'
ip_statuses = [entry['status'] for entry in data['ip_status']]

# Calculate the percentage of 'online' and 'offline' entries
total_count = len(ip_statuses)
status_counts = Counter(ip_statuses)
online_percentage = (status_counts.get("online", 0) / total_count) * 100
offline_percentage = (status_counts.get("offline", 0) / total_count) * 100

# Determine the status and create the status message
if online_percentage >= 20:
    status = "online"
    color = 0x57F287  # Green color for online
    emoji = "📱"
else:
    status = "offline"
    color = 0xED4245  # Red color for offline
    emoji = "📵"

offline_count = status_counts.get("offline", 0)
with open("status.txt", "w") as file:
    file.write(status)

try:
    # Make an API call to OpenWeather to get local weather in Gaza
    weather_response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Gaza&appid={openweather_api_key}")
    weather_response.raise_for_status()  # Raise an HTTPError for bad responses

    weather_data = weather_response.json()
    temperature_kelvin = weather_data["main"]["temp"]
    temperature_celsius = temperature_kelvin - 273.15  # Convert to Celsius

    # Get the local time for Gaza (assuming UTC+2)
    current_time = datetime.utcnow() + timedelta(hours=2)
    time_str = current_time.strftime("%H:%M:%S %Z\n%A, %d %B %Y")
    temperature_str = f"{temperature_celsius:.1f} °C"

    print(f"Weather in Gaza:")
    print(f"Temperature: {temperature_str}")
    print(f"Time: {time_str}")

except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
    print("Could not fetch weather information.")
# Create the Discord message payload
discord_payload = {
    "content": None,
    "embeds": [
        {
            "title": f"{online_percentage:.2f}% Online {emoji}",
            "description": f"Offline: {offline_count} / {total_count}",
            "color": color,
            "fields": [
                {
                    "name": "Local Time and Weather",
                    "value": f"```\n{time_str}\n\n{temperature_str}\n```"
                }
            ],
            "author": {
                "name": "Gaza IP Address Status",
                "url": "https://is-gaza.online/",
                "icon_url": "https://i.imgur.com/cIbuRkt.png"
            },
            "image": {
                "url": f"https://is-gaza.online/logs/{most_recent_png}"
        }
        }
    ],
    "attachments": []
}

# Your Discord webhook URL
webhook_url = discord_webhook_url

try:
    # Send the payload to the Discord webhook
    response = requests.post(webhook_url, json=discord_payload)

    # Check if the message was sent successfully
    if response.status_code == 204:
        print("Message sent to Discord successfully")
    else:
        print(f"Failed to send message to Discord. Status code: {response.status_code}")
except requests.exceptions.ConnectionError as e:
    print(f"Error while sending the message to Discord: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")