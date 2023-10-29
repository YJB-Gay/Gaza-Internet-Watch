import time
import subprocess

# Define the list of Python files to run in order
python_files = ['ping-ip.py', 'status.py', 'upload.py', 'update.py']

# Set the delay between each file execution in seconds
delay_between_files = 5

# Set the loop interval in seconds
loop_interval = 300  # 5 minutes

while True:
    for file in python_files:
        print(f"Running {file}")
        subprocess.run(["python", file])
        time.sleep(delay_between_files)
    
    print("Waiting for the next loop...")
    time.sleep(loop_interval)
