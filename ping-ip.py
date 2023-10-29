import concurrent.futures
from ping3 import ping
import json
from datetime import datetime
import pytz
import re
import os
import glob
import requests

# Maximum number of log files to keep
max_log_files = 10

# List of IP addresses to ping
ip_addresses = [
    "5.133.31.74",
    "213.6.139.114",
    "188.161.194.21",
    "188.161.165.182",
    "206.62.2.166",
    "5.133.29.240",
    "206.62.2.32",
    "206.62.2.49",
    "206.62.2.24",
    "206.62.2.200",
    "206.62.2.190",
    "206.62.2.216",
    "206.62.2.85",
    "206.62.2.110",
    "206.62.2.217",
    "206.62.2.45",
    "206.62.2.55",
    "206.62.2.35",
    "206.62.2.41",
    "206.62.2.25",
    "206.62.2.213",
    "206.62.2.141",
    "206.62.2.47",
    "206.62.2.172",
    "206.62.2.131",
    "206.62.2.20",
    "206.62.2.33",
    "206.62.2.39",
    "206.62.2.219",
    "206.62.2.21",
    "206.62.2.53",
    "206.62.2.240",
    "206.62.2.215",
    "206.62.2.255",
    "206.62.2.103",
    "206.62.2.30",
    "206.62.2.207",
    "5.133.24.13",
    "5.133.24.101",
    "5.133.24.123",
    "5.133.24.206",
    "5.133.24.223",
    "5.133.27.22",
    "5.133.30.68",
    "5.133.30.130",
    "5.133.30.150",
    "5.253.71.1",
    "37.8.0.0",
    "37.8.1.146",
    "37.8.3.238",
    "37.8.7.199",
    "37.8.7.217",
    "37.8.9.5",
    "37.8.12.76",
    "37.8.12.152",
    "37.8.16.207",
    "37.8.19.15",
    "37.8.22.111",
    "37.8.27.95",
    "37.8.83.113",
    "46.60.78.243",
    "46.60.82.130",
    "46.60.90.19",
    "82.205.14.244",
    "82.205.124.174",
    "83.244.23.226",
    "83.244.23.254",
    "83.244.112.122",
    "85.114.98.50",
    "85.114.98.147",
    "85.114.101.172",
    "85.114.105.126",
    "85.114.110.135",
    "85.114.115.1",
    "85.114.116.114",
    "85.114.119.6",
    "85.114.119.22",
    "85.114.121.1",
    "85.114.125.1",
    "85.114.127.1",
    "85.184.243.36",
    "85.184.243.155",
    "86.104.189.196",
    "89.239.32.41",
    "89.239.32.138",
    "89.239.34.0",
    "89.239.34.10",
    "89.239.40.202",
    "89.239.42.34",
    "94.26.116.33",
    "94.26.121.8",
    "94.26.126.220",
    "152.89.41.245",
    "152.89.42.140",
    "158.140.80.96",
    "158.140.89.13",
    "158.140.99.54",
    "158.140.110.87",
    "158.140.125.162",
    "176.58.65.35",
    "176.58.65.52",
    "176.65.0.0",
    "176.65.3.0",
    "176.65.10.46",
    "176.65.10.208",
    "176.65.15.16",
    "176.65.15.188",
    "185.40.194.232",
    "185.40.195.193",
    "185.132.249.2",
    "185.132.249.242",
    "185.132.250.236",
    "185.132.251.177",
    "185.132.251.230",
    "185.138.133.72",
    "188.161.0.0",
    "188.161.19.234",
    "188.161.23.236",
    "188.161.24.253",
    "188.161.27.11",
    "188.161.27.33",
    "188.161.78.158",
    "188.161.97.224",
    "188.161.123.254",
    "188.161.140.145",
    "188.161.161.177",
    "188.161.162.129",
    "188.161.195.225",
    "188.161.244.146",
    "188.161.245.60",
    "188.161.250.156",
    "188.225.253.155",
    "193.7.223.58",
    "193.7.223.158",
    # Add more IP addresses here
]

# Directory path for log files
log_directory = r"E:\Nicholas\Downloads\gaza_ip_test\Gaza-Internet-Watch\logs"

# Directory path for status.txt
status_directory = r"E:\Nicholas\Downloads\gaza_ip_test\Gaza-Internet-Watch"

def ping_ip(ip):
    result = ping(ip, timeout=2)  # Set a timeout of 2 seconds

    if result is not None:
        if result >= 0:
            return {"ip": ip, "status": "online"}
        else:
            return {"ip": ip, "status": "offline"}
    else:
        return {"ip": ip, "status": "offline"}

def main():
    online_count = 0
    offline_count = 0

    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(ping_ip, ip_addresses))

    for result in results:
        print(result)
        if result["status"] == "online":
            online_count += 1
        elif result["status"] == "offline":
            offline_count += 1

    total_count = len(ip_addresses)
    online_threshold = total_count // 2

    status = "online" if online_count >= online_threshold else "offline"

    # Create a timestamp with UTC+0 timezone
    timestamp = datetime.now(pytz.utc).strftime('%Y-%m-%d %H-%M-%S UTC')

    # Replace invalid characters and spaces in the timestamp
    timestamp = re.sub(r'[^\w-]', '_', timestamp)

    # Create a dictionary to store the results
    log_data = {
        "timestamp": timestamp,
        "status": status,
        "ip_status": results
    }

    # Generate a valid log filename with spaces replaced by underscores
    log_filename = f"Logs-{timestamp}.json"

    # Replace spaces with underscores in the filename
    log_filename = log_filename.replace(" ", "_")

    # Construct the full path for the log file
    log_file_path = os.path.join(log_directory, log_filename)

    # Write the results to a JSON file in the "logs" folder
    with open(log_file_path, "w") as log_file:
        json.dump(log_data, log_file, indent=4)

    # Delete older log files if the number of log files exceeds the maximum limit
    delete_old_logs()

    # Upload the log file to Catbox
    catbox_log_url = upload_file_to_catbox(log_file_path, "72h")
    print("Catbox URL for logs:", catbox_log_url)

    # Upload status.txt to Catbox
    status_filename = "status.txt"
    status_file_path = os.path.join(status_directory, status_filename)

    # Replace backslashes with forward slashes in the file path
    status_file_path = status_file_path.replace("\\", "/")

    catbox_status_url = upload_file_to_catbox(status_file_path, "72h")
    print("Catbox URL for status.txt:", catbox_status_url)

def delete_old_logs():
    # Get a list of log files in the "logs" folder
    log_files = glob.glob(os.path.join(log_directory, "Logs-*.json"))

    # Sort log files by creation time (oldest to newest)
    log_files.sort()

    # Check if the number of log files exceeds the maximum limit
    if len(log_files) > max_log_files:
        # Determine the number of files to delete
        num_files_to_delete = len(log_files) - max_log_files

        # Delete the oldest log files
        for i in range(num_files_to_delete):
            file_to_delete = log_files[i]
            os.remove(file_to_delete)
            print(f"Deleted old log file: {file_to_delete}")

def upload_file_to_catbox(file_path, time="72h"):
    catbox_url = "https://catbox.moe/user/api.php"
    
    try:
        with open(file_path, 'rb') as file:
            files = {'fileToUpload': (os.path.basename(file_path), file)}
            data = {'reqtype': 'fileupload', 'time': time}
            response = requests.post(catbox_url, data=data, files=files)
            response_data = response.json()
            if 'file' in response_data:
                return response_data['file']['url']
    except Exception as e:
        print(f"Error while uploading {file_path} to Catbox:", e)
    return None

if __name__ == "__main__":
    main()