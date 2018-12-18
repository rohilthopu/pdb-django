import json

import requests

import time

from dParse import getModifiers

link = "https://storage.googleapis.com/mirubot/paddata/processed/na_dungeons.json"

jsonz = requests.get(link).text

data = json.loads(jsonz)

vals = set()
vals2 = set()

l = []
l2 = []

v = 3
n = 40

pos = 8

for item in data:
    for floor in item['floors']:
        raw = floor['raw']
        # vals.add(raw[v])
        # vals2.add((raw[5]))

        while (int(raw[pos]) is not 0):
            pos += 1
        pos += 1
        vals.add(int(raw[pos]))
        pos = 8

for item in vals:
    l.append(int(item))

# for item in vals:
#     if item not in vals2:
#         print(item)

print(sorted(l))

print()

for item in data:
    for floor in item['floors']:
        raw = floor['raw']

        while (int(raw[pos]) is not 0):
            pos += 1
        pos += 1
        if int(raw[pos]) == n:
            # if int(raw[pos+1]) == 10:
            print(item['clean_name'], raw)

            rVal = getModifiers(raw, pos).entryRequirement
            #
            print(rVal)

        # if int(raw[5]) == n:
        #     print("\t\t", item['clean_name'])

        pos = 8
