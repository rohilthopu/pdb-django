import urllib
import requests
import lxml
import json
import datetime
import time
import pytz

link = "https://storage.googleapis.com/mirubot/paddata/merged/guerrilla_data.json"

req = requests.get(link).text
js = json.loads(req)
items = js['items']
for item in items:
    start = item['start_timestamp']
    conv = datetime.datetime.fromtimestamp(start, pytz.UTC)
    if item['group'] == "A":
        print(conv, item['dungeon_name'], item['group'])
