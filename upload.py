import glob
import requests
import os
import json

# Function to calculate the offline percentage
def calculate_offline_percentage(log_file_path):
    with open(log_file_path, "r") as log_file:
        log_data = json.load(log_file)

    status_counts = {"offline": 0}
    total_count = 0

    for entry in log_data['ip_status']:
        total_count += 1
        if entry['status'] == "offline":
            status_counts["offline"] += 1

    if total_count > 0:
        offline_percentage = (status_counts.get("offline", 0) / total_count) * 100
    else:
        offline_percentage = 0

    return offline_percentage

def find_most_recent_log():
    log_files = glob.glob(f"{logs_dir}/Logs-*.json")
    if not log_files:
        return None
    return max(log_files, key=os.path.getctime)

# Litterbox API endpoint
api_url = "https://litterbox.catbox.moe/resources/internals/api.php"
# File paths
txt_file_path = "status.txt"
logs_dir = "logs"

# Function to calculate the offline percentage
def calculate_offline_percentage(log_file_path):
    with open(log_file_path, "r") as log_file:
        log_data = json.load(log_file)

    status_counts = {"offline": 0}
    total_count = 0

    for entry in log_data['ip_status']:
        total_count += 1
        if entry['status'] == "offline":
            status_counts["offline"] += 1

    if total_count > 0:
        offline_percentage = (status_counts.get("offline", 0) / total_count) * 100
    else:
        offline_percentage = 0

    return offline_percentage

# Determine the most recent JSON file in the /logs directory
def get_most_recent_json_file():
    json_files = [f for f in os.listdir(logs_dir) if f.endswith(".json")]
    if json_files:
        return max(json_files, key=lambda x: os.path.getctime(os.path.join(logs_dir, x)))
    else:
        return None

# Upload a file to Litterbox and return the URL
def upload_to_litterbox(file_path, time):
    with open(file_path, 'rb') as file:
        files = {'fileToUpload': (os.path.basename(file_path), file)}
        data = {'reqtype': 'fileupload', 'time': time}
        response = requests.post(api_url, files=files, data=data)
        if response.status_code == 200:
            return response.text
        else:
            return None

# Main function
def main():
    most_recent_json_file = get_most_recent_json_file()

    if most_recent_json_file:
        # Upload status.txt to Litterbox for 12 hours
        txt_url = upload_to_litterbox(txt_file_path, '12h')

        if txt_url:
            # Upload the most recent JSON file to Litterbox for 24 hours
            json_url = upload_to_litterbox(os.path.join(logs_dir, most_recent_json_file), '24h')

            if json_url:
                # Store the URLs in cache.json
                cache_data = {
                    'txt_url': txt_url,
                    'json_url': json_url
                }

                with open('cache.json', 'w') as cache_file:
                    json.dump(cache_data, cache_file, indent=4)

                print("Files uploaded and URLs stored in cache.json.")
            else:
                print("Failed to upload the JSON file to Litterbox.")
        else:
            print("Failed to upload status.txt to Litterbox.")
    else:
        print("No JSON files found in the logs directory.")

if __name__ == "__main__":
    main()
