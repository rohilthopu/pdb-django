import json
from .dungeon import DungeonFloor, Dungeon
import os
import csv
from io import StringIO
from typing import List, Any


def get_dungeon_list() -> List[Dungeon]:

    with open(os.path.abspath('/home/rohil/data/pad_data/raw_data/na/download_dungeon_data.json'), 'r') as jsonPull:

        dungeons = json.load(jsonPull)
        dungeon_json = dungeons

        if dungeon_json['v'] > 6:
            print('Warning! Version of dungeon file is not tested: {}'.format(dungeon_json['v']))

        dungeon_info = dungeon_json['dungeons']

        dungeons = []
        cur_dungeon = None

        for line in dungeon_info.split('\n'):
            info = line[0:2]
            data = line[2:]
            data_values = next(csv.reader(StringIO(data), quotechar="'"))
            if info == 'd;':
                cur_dungeon = Dungeon(data_values)
                dungeons.append(cur_dungeon)
            elif info == 'f;':
                floor = DungeonFloor(data_values)
                cur_dungeon.floors.append(floor)
            elif info == 'c;':
                pass
            else:
                raise ValueError('unexpected line: ' + line)

        return dungeons
