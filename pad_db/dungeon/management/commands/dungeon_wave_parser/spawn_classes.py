import json


class EncounterItem:

    def __init__(self, raw):
        self.server = raw[1]
        self.dungeon_id = int(raw[2])
        self.floor_id = int(raw[3])
        self.wave = int(raw[4])
        self.slot = int(raw[5])

        # rare or not?
        self.spawn_type = 'rare' if int(raw[6]) == 1 else 'normal'

        self.monster_id = int(raw[7])
        self.monster_level = int(raw[8])
        self.drop_id = int(raw[9])
        self.drop_monster_level = int(raw[10])


class JsonDictEncodable(json.JSONEncoder):
    """Utility parent class that makes the child JSON encodable."""

    def default(self, o):
        return o.__dict__

    def __str__(self):
        return str(self.__dict__)


class Monster(JsonDictEncodable):
    def __init__(self, monster_id):
        self.card_id = monster_id
        self.monster_data = None


class Wave(JsonDictEncodable):
    def __init__(self, wave_number):
        self.wave = wave_number
        self.encounter_list = []


class Floor(JsonDictEncodable):
    def __init__(self, floor_number):
        self.floor = floor_number
        self.waves = []

class Dungeon(JsonDictEncodable):
    def __init__(self, dungeon_id):
        self.dungeon_id = dungeon_id
        self.floors = []
