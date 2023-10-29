import requests
import os
import json

# Litterbox API endpoint
api_url = "https://litterbox.catbox.moe/resources/internals/api.php"

# File paths
txt_file_path = "status.txt"
logs_dir = "logs"

# Determine the most recent JSON file in the /logs directory
def get_most_recent_json_file():
    json_files = [f for f in os.listdir(logs_dir) if f.endswith(".json")]
    if json_files:
        return max(json_files, key=lambda x: os.path.getctime(os.path.join(logs_dir, x)))
    else:
        return None

# Count "offline" entries in the JSON file
def count_offline_entries(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        offline_count = sum(1 for entry in data['ip_status'] if entry['status'] == "offline")
        total_count = len(data['ip_status'])
        return offline_count, total_count

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
        # Count "offline" entries in the most recent JSON file
        offline_count, total_count = count_offline_entries(os.path.join(logs_dir, most_recent_json_file))

        # Upload status.txt to Litterbox for 12 hours
        txt_url = upload_to_litterbox(txt_file_path, '12h')

        if txt_url:
            # Upload the most recent JSON file to Litterbox for 24 hours
            json_url = upload_to_litterbox(os.path.join(logs_dir, most_recent_json_file), '24h')

            if json_url:
                # Store the URLs and count in cache.json
                cache_data = {
                    'txt_url': txt_url,
                    'json_url': json_url,
                    'count': f"{offline_count} / {total_count}"
                }

                with open('cache.json', 'w') as cache_file:
                    json.dump(cache_data, cache_file, indent=4)

                print("Files uploaded, and URLs and count stored in cache.json.")
            else:
                print("Failed to upload the JSON file to Litterbox.")
        else:
            print("Failed to upload status.txt to Litterbox.")
    else:
        print("No JSON files found in the logs directory.")

if __name__ == "__main__":
    main()
