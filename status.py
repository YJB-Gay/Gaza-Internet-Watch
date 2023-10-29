import os
import json
from collections import Counter

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

# Determine the status based on the percentages
if online_percentage >= 50:
    status = "online"
else:
    status = "offline"

# Create the 'status.txt' file with the determined status
with open("status.txt", "w") as status_file:
    status_file.write(status)

print(f"Status: {status}")
