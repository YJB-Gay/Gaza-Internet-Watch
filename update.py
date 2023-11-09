import json
import os
import csv
import datetime
import plotly.express as px
import pandas as pd
import time

current_unix_timestamp = int(time.time())

logs_dir = "logs"
offline_count = 0
total_count = 0
json_url = ""  
txt_url = "https://is-gaza.online/status.txt"
online_url = "https://files.catbox.moe/b1v3v1.png"
offline_url = "https://files.catbox.moe/4mbxbo.png"
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
def main():
    global offline_count, total_count, json_url, favicon_url
    most_recent_json_file = get_most_recent_json_file()
    if most_recent_json_file:
        offline_count, total_count = count_offline_entries(os.path.join(logs_dir, most_recent_json_file))
        json_url = f"https://is-gaza.online/logs/{most_recent_json_file}"
        if offline_count / total_count >= 0.2:
            favicon_url = offline_url
        else:
            favicon_url = online_url

if __name__ == "__main__":
    main()


count = f"{offline_count} / {total_count}"
def update_csv(filename, offline_count, total_count):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    percent_online = round(((total_count - offline_count) / total_count) * 100, 2)
    online_count = total_count - offline_count
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, online_count, offline_count, total_count, percent_online])
if __name__ == "__main__":
    csv_filename = r'chart\data.csv'
    update_csv(csv_filename, offline_count, total_count)
data = {"json_url": json_url}
with open("cache.json", "w") as file:
    json.dump(data, file)
df = pd.read_csv("Chart/data.csv")
fig = px.line(df, x="Timestamp", y="Percent Online", title="Gaza Internet Status (Based on 2,437 IPs in the Gaza Strip)")
fig.update_layout(template="plotly_dark")
fig.write_html("chart/index.html")    
fig.write_image("chart/chart.png")
with open('chart/index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
head_content = """
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width"/>
    <meta name="theme-color" content="#118a84"/>
    <meta property="og:title" content="Gaza Internet Chart"/>
    <meta property="og:description" content="Gaza Internet Status (Based on 2,437 IPs in the Gaza Strip)"/>
    <meta property="og:image" content="https://files.catbox.moe/4ledo4.jpg"/>
    <meta name="twitter:card" content="summary_large_image"/>
    <meta name="twitter:image" content={`https://is-gaza.online/chart/chart.png?${current_unix_timestamp}`}/>
    <meta name="next-head-count" content="8"/>
"""
head_start = html_content.find('<head>')
head_end = html_content.find('</head>') + 7 
modified_html = html_content[:head_end] + head_content + html_content[head_end:]
with open('chart/index.html', 'w', encoding='utf-8') as file:
    file.write(modified_html)

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="300"> 
    <meta charset="utf-8">
    <title>Gaza Internet Watch</title>
    <link rel="icon" href="{favicon_url}">
    <meta name="description" content="Based on 2,437 IPs in the Gaza Strip">
    <meta property="og:title" content="Gaza Internet Watch">
    <meta property="og:description" content="Based on 2,437 IPs in the Gaza Strip">
    <meta property="og:image" content="https://files.catbox.moe/4ledo4.jpg">
<head>
    <title>Gaza Internet Watch</title>
    <style>
        body {{
            background-image: url('https://files.catbox.moe/26caxg');
            background-size: cover;
            backdrop-filter: blur(0px);
            color: #ffffff;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }}
        h1 {{
            font-size: 72px; /* 3x bigger */
        }}
        p {{
            font-size: 48px; /* Same size as Online/Offline text */
        }}
        #status {{
            font-size: 72px; /* 3x bigger */
            color: green;
        }}
        #status.offline {{
            color: red;
        }}
        #additional-info {{
            font-size: 24px; /* Smaller text */
        }}
        #more-info {{
            font-size: 18px; /* Even smaller text */
        }}
        #donate-button {{
            background-color: #0074d9;
            color: #ffffff;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            position: fixed;
            bottom: 20px;
            left: 20px;
        }}
        #image-credit {{
            color: #ffffff;
            text-decoration: none;
            position: absolute;
            bottom: 20px;
            right: 20px;
        }}
        #contact-button {{
            background-color: #0074d9;
            color: #ffffff;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            position: fixed;
            bottom: 70px;
            left: 20px;
        }}
        
    </style>
    <script>
        function checkStatus() {{
            fetch('{txt_url}')
                .then(response => response.text())
                .then(data => {{
                    if (data.trim() === 'online') {{
                        document.getElementById('status').textContent = 'Online';
                    }} else {{
                        document.getElementById('status').textContent = 'Offline';
                        document.getElementById('status').classList.add('offline');
                    }}
                }})
                .catch(error => {{
                    document.getElementById('status').textContent = 'Error';
                    document.getElementById('status').classList.add('offline');
                }});
        }}
    </script>
</head>
<body style="margin: 0; padding: 0;">
    <h1 style="margin: 0;">Gaza Internet</h1>
    <p style="margin: 0;">Status: <span id="status">Checking...</span></p>
    <p style="margin: 0;">Based on 2,437 IPs in the Gaza Strip</p>
    <p id="count" style="font-size: 24px; margin: 0; padding: 0; line-height: 1.2;">Count Offline: {count}</p>
    <p style="margin: 0; font-size: 16px;">The status will be considered offline if less than 20% of the IP addresses are online.</p>
    <p style="margin: 0; font-size: 16px;"><a href="{json_url}" style="font-size: 16px;">Logs</a></p>
    
    <div>
        <a id="donate-button" href="/donate/">Donate To Save Gaza</a>
        <a id="image-credit" href="https://www.instagram.com/alijadallah66">Image credit Ali Jadallah - علي جادالله</a>
        <a id="contact-button" href="mailto:contact@is-gaza.online">Contact</a>
    </div>
    
    </div>
    <script>
        checkStatus();
    </script>
</body>
</html>
"""

# Save the HTML content to index.html with UTF-8 encoding
with open('index.html', 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

print("HTML file updated successfully.")
