DUNGEON_TYPE = {
    0: 'Normal Dungeon',
    1: 'Special Dungeon',
    2: 'Technical Dungeon',
    3: 'Gift Dungeon',
    4: 'Tournament Dungeon',
    5: 'Special Descended Dungeon',
    7: 'Multiplayer Dungeon',
}


DUNGEON_TYPE_DESCRIPTORS = {
    0: 'Normal', # Something to do with them at least
    1: 'Special Descended',
    2: 'Endless',
    23101: 'Alt. Technical',
    23111: "Last Technical", # Before the "Legendary Series"
    31001: 'Annihilation Technical',
    31002: 'Annihilation Descended',
    32001: 'Endless',
    30001: 'Challenge Machine Technical', # When there are MZeus/Hera/Etc in the Challenge Series
    30002: 'Descended Rush',
    30011: 'Arena', # Specifically Ultimate and Alt. Ultimate
    30012: 'Super Ultimate Colosseum',
    38908: 'The Thief Descended', # Only
    49001: 'One-Shot Challenge',
    60001: 'Daily Descend', # I think, as in, are in the daily rotation?
    60002: 'One-Shot Challenge',
    60102: 'Metal Dragon',
    150001: 'King Carnival',
    200011: 'Mythical Endless Corridors',
    200207: 'Super Ultimate Dragon Rush',
    200601: 'Machine Technical',
    201902: "Ultimate Yamato Rush (alpha)",
    202002: "Super Ultimate Devil Rush (alpha)",
    210001: 'Coin',
    210002: 'Challenge',
    210004: "PAD Academy",
    210006: 'Time Attack Dungeon',
    210011: 'Collab',
    210051: 'Event Challenge',
    220001: 'Challenge',
    290001: 'Monthly Quest',
    299902: 'Tues-Fri Dungeon',
    299911: 'Metal Dragon',
    300001: 'Daily',
    400001: 'Guerrilla',
    490001: 'GachaDra',
    500001: 'Gift/Daily Event',
    500011: 'Gift/Daily Event',
    600001: 'Multiplayer Endless Corridors',
    600002: 'Multiplayer Evo Rush',
    600003: 'Multiplayer Descended',
    600004: 'Multiplayer Special Descended',

    600011: 'Multiplayer',
}


REPEAT_DAY = {
    0: None,
    1:'Monday',
    2:'Tuesday',
    3:'Wednesday',
    4:'Thursday',
    5:'Friday',
    8:'Weekend'
}


def get_dungeon_type(val: int, name: str) -> str:

    if val in range(5611, 5615):
        return "Retired Special Dungeons" # These are the last normal dungeons
    elif val in range(21612, 21618):
        return "Technical"
    elif val in range(38901, 38912):
        return "Descended (original)"
    elif val in range(200101,200111):
        return "Alt. Technial"
    elif val in range(200021,200057):
        return "Technical"
    elif val in range(200301, 200306) or val in range(200201,200206):
        return "Special Decended"
    elif val in DUNGEON_TYPE_DESCRIPTORS:
        return DUNGEON_TYPE_DESCRIPTORS[val]
    else:
        return name, " : ", val, "is not registered."
