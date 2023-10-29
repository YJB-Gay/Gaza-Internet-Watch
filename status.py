import os
import json
from collections import Counter
import requests

# Define the folder where the JSON files are located
log_folder = "logs"

# List all JSON files in the folder
json_files = [f for f in os.listdir(log_folder) if f.endswith(".json")]

# Sort the files by modification time and get the most recent one
most_recent_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(log_folder, f))

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

# Determine the status based on the percentages
if online_percentage >= 50:
    status = "online"
    color = 0x57F287  # Green color
    emoji = "📱"
else:
    status = "offline"
    color = 0xED4245  # Red color
    emoji = "📵"

# Make a request to OpenWeather API to get weather information for Gaza
openweather_api_key = "f0b8d86c7277f1c4d0d7bcd7efd92862"
response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Gaza&appid={openweather_api_key}")
weather_data = response.json()
temperature = weather_data['main']['temp'] - 273.15  # Convert temperature to Celsius
local_time = "21:13:28 EEST"  # Replace with the actual local time

# Create the 'status.txt' file with the determined status
with open("status.txt", "w") as status_file:
    status_file.write(status)

# Create the Discord message
discord_webhook_url = "https://canary.discord.com/api/webhooks/1167614630957420634/F2IU3zXqV2rdk1SbLnHvpZbhBtUEc2K2zOLL-_hpSKjwt6b6tkNou0M6UGVTXkx6j_Y3"
payload = {
    "embeds": [
        {
            "title": f"{online_percentage:.2f}% {status} {emoji}",
            "description": f"**Local Time and Weather**\n```\n{local_time}\nSaturday, 28 October 2023\n\n{temperature:.1f} °C\n```",
            "color": color,
            "author": {
                "name": "Gaza IP Address Status",
                "icon_url": "https://i.imgur.com/cIbuRkt.png"
            }
        }
    ]
}

response = requests.post(discord_webhook_url, json=payload)

print(f"Status: {status}")