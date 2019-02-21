import csv
import json
import os

from spawn_classes import EncounterItem, Monster, Wave, Floor, Dungeon


def make_default_monster(encounter_item):
    return {'appearance_count': 0,
            'drop_count': 0,
            'drop_monsters': [encounter_item.drop_id] if encounter_item.drop_id != 0 else [],
            'average_monster_level': encounter_item.monster_level,
            'average_drop_level': encounter_item.drop_monster_level,
            'spawn_type': encounter_item.spawn_type,
            'slot': encounter_item.slot,
            }


def make_default_wave(encounter_item):
    return {encounter_item.monster_id: make_default_monster(encounter_item)}


def make_default_floor(encounter_item):
    return {encounter_item.wave: make_default_wave(encounter_item)}


def make_default_dungeon(encounter_item):
    return {encounter_item.floor_id: make_default_floor(encounter_item)}


dungeons = {}

with open(os.path.abspath('/home/rohil/data/pad_data/processed_data/wave_data.csv'), 'r') as raw_data:
    data = csv.reader(raw_data)
    next(data, None)

    for item in data:
        raw = item

        encounter_item = EncounterItem(raw)

        if encounter_item.dungeon_id in dungeons:

            dungeon_floors = dungeons[encounter_item.dungeon_id]

            if encounter_item.floor_id in dungeon_floors:

                # dict of waves : floor data
                wave_list = dungeon_floors[encounter_item.floor_id]

                if encounter_item.wave in wave_list:

                    # get the monster list for the current wave to add a new monster into it
                    # dict monster_id : {}
                    wave_monster_list = wave_list[encounter_item.wave]

                    # if the monster is in the monster list
                    if encounter_item.monster_id in wave_monster_list:

                        # get the monster data for the existing monster
                        # this is a dict
                        monster = wave_monster_list[encounter_item.monster_id]

                        if encounter_item.monster_level != 0:
                            if monster['average_monster_level'] == 0:
                                monster['average_monster_level'] = encounter_item.monster_level
                            else:
                                monster_level_sum = monster['average_monster_level'] * monster['appearance_count']
                                monster['average_monster_level'] = round(float(
                                    (encounter_item.monster_level + monster_level_sum) / (
                                            monster['appearance_count'] + 1)), 2)

                        if encounter_item.drop_id != 0:

                            # save the drop
                            if encounter_item.drop_id not in monster['drop_monsters']:
                                monster['drop_monsters'].append(encounter_item.drop_id)

                            if encounter_item.drop_monster_level != 0:
                                if monster['average_drop_level'] == 0:
                                    monster['average_drop_level'] = encounter_item.drop_monster_level
                                else:
                                    monster_level_sum = monster['average_drop_level'] * monster['drop_count']
                                    monster['average_drop_level'] = round(float(
                                        (encounter_item.drop_monster_level + monster_level_sum) / (
                                                monster['drop_count'] + 1)), 2)

                            # increase the run counter
                            monster['appearance_count'] += 1
                            monster['drop_count'] += 1
                            monster['relative_drop_chance'] = round(
                                float(monster['drop_count'] / monster['appearance_count']), 2)

                        else:
                            # just up the run counter
                            monster['appearance_count'] += 1
                            monster['relative_drop_chance'] = round(
                                float(monster['drop_count'] / monster['appearance_count']), 2)
                    else:
                        wave_monster_list[encounter_item.monster_id] = make_default_monster(encounter_item)
                # make a wave dict for it
                else:
                    wave_list[encounter_item.wave] = make_default_wave(encounter_item)
            else:
                dungeon_floors[encounter_item.floor_id] = make_default_floor(encounter_item)
        else:
            dungeons[encounter_item.dungeon_id] = make_default_dungeon(encounter_item)

    parsed_dungeons = []

    for dungeon_id, floor_data in dungeons.items():

        dungeon = Dungeon(dungeon_id)

        for floor_number, wave_data in floor_data.items():

            floor = Floor(floor_number)

            for wave_number, monster_data in wave_data.items():

                wave = Wave(wave_number)

                for monster_id, data in monster_data.items():
                    monster = Monster(monster_id)
                    monster.monster_data = data
                    wave.encounter_list.append(monster)

                floor.waves.append(wave)

            dungeon.floors.append(floor)

        parsed_dungeons.append(dungeon)

    # this outputs in the following order:
    # dungeon_id -> floor_id -> wave -> monster_id -> monster_data
    with open(os.path.abspath('/home/rohil/data/pad_data/processed_data/wave_data.json'), 'w') as f:
        json.dump(parsed_dungeons, f, sort_keys=True, default=lambda x: x.__dict__, indent=4)
