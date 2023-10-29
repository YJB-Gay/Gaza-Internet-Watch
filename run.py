import time
import subprocess

# Define the list of Python files to run in order
python_files = ['ping-ip.py', 'status.py', 'upload.py', 'update.py']

# Set the delay between each file execution in seconds
delay_between_files = 5

# Set the loop interval in seconds
loop_interval = 300  # 5 minutes

# Specify the Git commit message
commit_message = "Automated script run and Git force push"

while True:
    for file in python_files:
        print(f"Running {file}")
        subprocess.run(["python", file])
        time.sleep(delay_between_files)

    # Fetch changes from the remote repository (origin)
    try:
        subprocess.run(["git", "fetch", "origin"])
        print("Git fetch from origin successful.")
    except Exception as e:
        print(f"Error during Git fetch from origin: {str(e)}")

    # Perform a Git force push to the origin
    try:
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", commit_message])
        subprocess.run(["git", "push", "--force"])
        print("Git force push to origin successful.")
    except Exception as e:
        print(f"Error during Git force push to origin: {str(e)}")

    print("Waiting for the next loop...")
    time.sleep(loop_interval)
