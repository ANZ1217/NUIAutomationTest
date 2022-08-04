import os
import subprocess
import re
import sys
import time

def run_command(command):
    print("command=", command)
    stream = os.popen(command)
    output = stream.read()
    print("output=", output)

# Start scrip here
run_command("sdb root on")
run_command("sdb devices")
run_command("sdb forward tcp:50051 tcp:50051")
run_command('sdb shell "app_launcher -k org.tizen.aurum-bootstrap"')
run_command('sdb shell "app_launcher -s org.tizen.aurum-bootstrap"')
# Wait 1 sec till bootstrap launched
time.sleep(1)
