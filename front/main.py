import csv
import time
import sys, os
import threading
from flask import Flask, jsonify, render_template
from pathlib import Path

data = {}
apps = []
logs_files = []


if getattr(sys, 'frozen', False):
    BASE_PATH = Path(sys.executable).parent
else:
    BASE_PATH = Path(__file__).parent

logs_location = BASE_PATH / "logs"

if not logs_location.exists():
    logs_location.mkdir(parents=True)


def search_for_logs():
    for logs in os.listdir(logs_location):
        if logs.endswith('.csv'):
            logs_files.append(logs)

def read_data():
    while True:
        try:
            for log in logs_files:
                data[log[4:-4]] = {}
                log_location = os.path.join(logs_location, log)
                with open(log_location, newline='', encoding='utf-8') as logs:
                    readed = csv.reader(logs, delimiter=',')
                    for line in readed:
                        data[log[4:-4]][line[0]] = (line[1], line[2])
                        apps.append(line[0])
            time.sleep(1)
        except KeyboardInterrupt:
            print("Closing the program.")
            sys.exit(1)

def capitalize_first(text_to_capitalize):
    out = ""
    for char_number, character in enumerate(text_to_capitalize):
        if char_number == 0:
            out = character.upper()
        else:
            out += character
    return out

def logs_manager():
    search_for_logs()
    read_t = threading.Thread(target=read_data, daemon=True)
    read_t.start()

    while read_t.is_alive():
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("Stopping the program...")
            sys.exit(1)

log_thread = threading.Thread(target=logs_manager, daemon=True)
log_thread.start()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html"), 200

@app.route('/stats')
def stats():
    return jsonify(data), 200

while log_thread.is_alive():
    try:
        app.run(host='0.0.0.0', port=5010, debug=False)
    except KeyboardInterrupt:
        print("Stopping all...")
        sys.exit(1)
