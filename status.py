import os
import json
import requests
from collections import Counter
from datetime import datetime, timedelta

# Define the folder where the JSON files are located
log_folder = "logs"

# List all JSON files in the folder
json_files = [f for f in os.listdir(log_folder) if f.endswith(".json")]

# Sort the files by modification time and get the most recent one
most_recent_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(log_folder, f)))

# Read the most recent JSON file
with open(os.path.join(log_folder, most_recent_file), 'r') as file:
    data = json.load(file)

# Extract the 'status' field from each entry in 'ip_status'
ip_statuses = [entry['status'] for entry in data['ip_status']]

# Calculate the percentage of 'online' and 'offline' entries
total_count = len(ip_statuses)
status_counts = Counter(ip_statuses)
online_percentage = (status_counts.get("online", 0) / total_count) * 100
offline_percentage = (status_counts.get("offline", 0) / total_count) * 100

# Determine the status and create the status message
if online_percentage >= 50:
    status = "online"
    color = 0x57F287  # Green color for online
    emoji = "📱"
else:
    status = "offline"
    color = 0xED4245  # Red color for offline
    emoji = "📵"

offline_count = status_counts.get("offline", 0)

# Make an API call to OpenWeather to get local weather in Gaza
openweather_api_key = "f0b8d86c7277f1c4d0d7bcd7efd92862"
weather_response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Gaza&appid={openweather_api_key}")
weather_data = weather_response.json()
temperature_kelvin = weather_data["main"]["temp"]
temperature_celsius = temperature_kelvin - 273.15  # Convert to Celsius
# Get the local time for Gaza (assuming UTC+2)
current_time = datetime.utcnow() + timedelta(hours=2)
time_str = current_time.strftime("%H:%M:%S %Z\n%A, %d %B %Y")
temperature_str = f"{temperature_celsius:.1f} °C"

# Create the Discord message payload
discord_payload = {
    "content": None,
    "embeds": [
        {
            "title": f"{online_percentage:.2f}% {status} {emoji}",
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
                "icon_url": "https://i.imgur.com/cIbuRkt.png"
            }
        }
    ],
    "attachments": []
}

# Your Discord webhook URL
webhook_url = "https://canary.discord.com/api/webhooks/1167614630957420634/F2IU3zXqV2rdk1SbLnHvpZbhBtUEc2K2zOLL-_hpSKjwt6b6tkNou0M6UGVTXkx6j_Y3"

# Send the payload to the Discord webhook
response = requests.post(webhook_url, json=discord_payload)

# Check if the message was sent successfully
if response.status_code == 204:
    print("Message sent to Discord successfully")
else:
    print(f"Failed to send message to Discord. Status code: {response.status_code}")
