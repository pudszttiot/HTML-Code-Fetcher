import subprocess

# Replace 'target_script.py' with the name of the Python script you want to open
script_to_open = 'homepage.py'

try:
    # Run the target script in the background without showing the command prompt
    subprocess.Popen(['python', script_to_open], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except FileNotFoundError:
    print(f"Error: The '{script_to_open}' file was not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
