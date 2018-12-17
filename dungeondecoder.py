import json

import requests

link = "https://storage.googleapis.com/mirubot/paddata/processed/na_dungeons.json"

jsonz = requests.get(link).text

data = json.loads(jsonz)

vals = set()
vals2 = set()

l = []
l2 = []

for item in data:
    for floor in item['floors']:
        raw = floor['raw']
        vals.add(raw[6])
        vals2.add((raw[5]))

for item in vals:
    l.append(int(item))

for item in vals2:
    l2.append(int(item))


for item in vals:
    if item not in vals2:
        print(item)

print(sorted(l2))
print(sorted(l))
print()

for item in data:
    for floor in item['floors']:
        raw = floor['raw']

        n = 11

        if int(raw[6]) == n:
            print(item['clean_name'])
        if int(raw[5]) == n:
            print("\t\t", item['clean_name'])
