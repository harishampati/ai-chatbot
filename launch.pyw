"""
launch.pyw – Double-click launcher for Aria chatbot.
Starts the Flask server silently, waits for it to be ready,
then opens the browser. The .pyw extension means no console window appears.
"""
import subprocess
import sys
import time
import webbrowser
import urllib.request
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URL = "http://127.0.0.1:5000"

# Start Flask in the background (no console window)
proc = subprocess.Popen(
    [sys.executable, os.path.join(BASE_DIR, "app.py")],
    cwd=BASE_DIR,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW,
)

# Wait until Flask is accepting connections (max 15 seconds)
for _ in range(30):
    try:
        urllib.request.urlopen(URL, timeout=1)
        break
    except Exception:
        time.sleep(0.5)

# Open the chatbot in the default browser
webbrowser.open(URL)
