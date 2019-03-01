import csv

with open('wave.csv', 'r') as wave_file:
    data = csv.reader(wave_file)
    next(data, None)

    for item in data:
        dungeon_id = item[0]
