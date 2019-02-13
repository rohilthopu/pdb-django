ATTRIBUTE_MAP = {
    -1: 'a random attribute of',
    0: 'fire',
    1: 'water',
    2: 'wood',
    3: 'light',
    4: 'dark',
    5: 'heart',
    6: 'jammer',
    7: 'poison',
    8: 'mortal poison',
}

# this is separate from the one above. specifies what types damage is reduced

DAMAGE_REDUCE_ATTRIBUTE_MAP = {
    1: 'fire',
    2: 'water',
    3: 'fire and water',
    4: 'wood',
    5: 'fire and wood',
    6: 'wood and water',
    8: 'light',
    9: 'fire and light',
    10: 'water and light',
    12: 'light and wood',
    13: 'fire, wood, and light',
    16: 'dark',
    17: 'dark and fire',
    18: 'water and dark',
    19: 'fire, water and dark',
    20: 'dark and wood',
    22: 'water, wood, and dark',
    24: 'light and dark',
    26: 'water, light and dark',
    28: 'wood, light, and dark',

}

TYPE_MAP = {
    -1: 0,  # Not set
    0: 7,  # Evolve
    1: 2,  # Balance
    2: 3,  # Physical
    3: 4,  # Healer
    4: 1,  # Dragon
    5: 6,  # God
    6: 5,  # Attacker
    7: 10,  # Devil
    8: 14,  # Machine
    12: 13,  # Awoken
    14: 8,  # Enhance
    15: 15,  # Vendor
}

EXPLICIT_TYPE_MAP = {
    0: "",  # Not set
    7: "Evo Material",  # Evolve
    2: "Balanced",  # Balance
    3: "Physical",  # Physical
    4: "Healer",  # Healer
    1: "Dragon",  # Dragon
    6: "God",  # God
    5: "Attacker",  # Attacker
    10: "Devil",  # Devil
    14: "Machine",  # Machine
    13: "Awoken Material",  # Awoken
    8: "Enhance Material",  # Enhance
    15: "Vendor",  # Vendor
}

COLUMN_MAP = {
    1: 'leftmost',
    2: 'second from the left',
    4: 'third from the left',
    8: 'third from the right',
    16: 'second from the right',
    32: 'rightmost'

}


class EnemySkill:
    def __init__(self):
        self.skill_id = -1
        self.name = ""
        self.effect = "No effect"
        self.skill_type = -1

    def __str__(self):
        return str(self.__dict__)


def get_skill_from_id(skill_id: str) -> EnemySkill:
    if skill_id in skill_lookup_map:
        return parse_skill(skill_lookup_map[skill_id])
    else:
        return None


def get_attrs_from_shift(val: int) -> []:
    attrs = []
    for i in range(0, 32):
        if val == -1:
            attrs.append(ATTRIBUTE_MAP[-1])
            break
        elif val & (1 << i):
            attrs.append(ATTRIBUTE_MAP[i])
    return attrs


def get_types_from_shift(val: int) -> []:
    attrs = []
    for i in range(0, 32):
        if val & (1 << i):
            attrs.append(EXPLICIT_TYPE_MAP[TYPE_MAP[i]])
    return attrs


def get_orb_change_location(rows: list) -> []:
    vals = []

    # this gets the rows bit list to be of length 5 to make a proper board
    if len(rows) is not 5:
        for i in range(0, 5 - len(rows)):
            rows.append('0')

    for row in rows:
        orbs = []
        for i in range(0, 6):
            if (int(row) & (1 << i)) != 0:
                orbs.append('X')
            else:
                orbs.append('-')
        vals.append(orbs)

    return vals


# todo list : 76 - 80
# possibly update: 2, 72, 94, 97

def make_effect(skill_type: int, s: EnemySkill, skill_data: list):
    if skill_type == 1:
        min_turns = int(skill_data[3])
        max_turns = int(skill_data[4])

        if min_turns == max_turns:
            turns = "{} turn(s)".format(min_turns)
        else:
            turns = "{} to {} turn(s)".format(min_turns, max_turns)
        s.effect = "Binds {} teammate(s) for {}".format(skill_data[2], turns)
    elif skill_type == 2:
        min_turns = skill_data[2]
        max_turns = skill_data[3]

        if min_turns == max_turns:
            turns = "{} turn(s)".format(min_turns)
        else:
            turns = "{} to {} turn(s)".format(min_turns, max_turns)

        s.effect = "Binds teammates for {}".format(turns)

    elif skill_type == 3:
        bound_type = EXPLICIT_TYPE_MAP[TYPE_MAP[int(skill_data[2])]]
        turns = skill_data[3]
        s.effect = "Binds {} type teammates for {} turn(s)".format(bound_type, turns)
    elif skill_type == 4:
        if len(skill_data) == 3:
            # special case
            attr1 = ATTRIBUTE_MAP[int(skill_data[1])]
            attr2 = ATTRIBUTE_MAP[int(skill_data[2])]
        else:
            attr1 = ATTRIBUTE_MAP[int(skill_data[2])]
            attr2 = ATTRIBUTE_MAP[int(skill_data[3])]

        s.effect = "Changes {} orbs to {} orbs".format(attr1, attr2)
    elif skill_type == 5:
        s.effect = "Blinds the board"
    elif skill_type == 12:
        # this is a one-off
        s.effect = "Changes fire orbs to jammers"
    elif skill_type == 13:
        s.effect = "Changes {} random attribute orbs to jammers".format(skill_data[2])
    elif skill_type == 15:
        s.effect = "Deals {}% damage {} time(s)".format(skill_data[4], skill_data[2])
    elif skill_type == 19:
        s.effect = "Attack becomes {}% for {} turns".format(skill_data[4], skill_data[3])
    elif skill_type == 40:
        s.effect = "Self-destruct"
    elif skill_type == 48:

        length = len(skill_data)

        if length == 4:
            s.effect = "Hits for {}% ATK and changes all orbs to {} orbs".format(skill_data[2],
                                                                                 ATTRIBUTE_MAP[int(skill_data[3])])
        else:
            s.effect = "Hits for {}% ATK and changes {} orbs to {} orbs".format(skill_data[2],
                                                                                ATTRIBUTE_MAP[int(skill_data[3])],
                                                                                ', '.join(get_attrs_from_shift(
                                                                                    int(skill_data[4]))))
    elif skill_type == 50:
        s.effect = "Gravity attack for {}% of players health".format(skill_data[2])
    elif skill_type == 52:
        s.effect = "Revives defeated teammate to {}% health".format(skill_data[2])
    elif skill_type == 56:
        s.effect = "Changes {} orbs to poison".format(ATTRIBUTE_MAP[int(skill_data[2])])
    elif skill_type == 60:
        s.effect = "Changes {} random orbs to poison".format(skill_data[2])
    elif skill_type == 61:
        s.effect = "Changes {} random orbs to mortal poison".format(skill_data[2])
    elif skill_type == 62:
        s.effect = "Blinds the board and hits for {}% ATK".format(skill_data[2])
    elif skill_type == 63:
        min_turns = int(skill_data[3])
        max_turns = int(skill_data[4])

        if min_turns == max_turns:
            turns = "{} turn(s)".format(min_turns)
        else:
            turns = "{} to {} turns".format(min_turns, max_turns)

        length = len(skill_data)

        if length == 6:
            num_teammates = skill_data[-1]
        elif length >= 7:
            num_teammates = skill_data[-2]
        else:
            # fallback condition to come back to
            num_teammates = 1
        if int(num_teammates) == 6:
            bind_description = "all monsters"
        else:
            bind_description = "{} random teammate(s)".format(num_teammates)

        s.effect = "Hits for {}% ATK and binds {} for {}".format(skill_data[2], bind_description, turns)

    elif skill_type == 64:
        s.effect = "Hits for {}% ATK and changes {} random orb(s) to poison".format(skill_data[2], skill_data[3])

    elif skill_type == 65:
        min_turns = int(skill_data[3])
        max_turns = int(skill_data[4])

        if min_turns == max_turns:
            turns = "{} turn(s)".format(min_turns)
        else:
            turns = "{} to {} turns".format(min_turns, max_turns)
        s.effect = "Binds {} random sub teammate(s) for {}".format(skill_data[2], turns)

    elif skill_type == 68:
        # special case
        s.effect = "Fire orbs more likely to appear for 99 turns"
    elif skill_type == 69:
        s.effect = "This monster transforms upon defeat"
    elif skill_type == 72:

        flag = int(skill_data[-2])
        s.effect = "Reduces incoming {} damage by {}%".format(DAMAGE_REDUCE_ATTRIBUTE_MAP[flag],
                                                              skill_data[-1])
    elif skill_type == 73:
        s.effect = "Will survive killing blows when HP is above {}% (resolve)".format(skill_data[-1])
    elif skill_type == 74:
        s.effect = "Reduces incoming damage by {}% for {} turn(s)".format(skill_data[3], skill_data[2])
    elif skill_type == 81:
        attrs = skill_data[3: skill_data.index('-1')]
        attr_str = ', '.join([ATTRIBUTE_MAP[int(item) - 1] for item in attrs]) if len(attrs) > 0 else 'unknown'
        s.effect = 'Hits for {}% ATK and changes all orbs to {}'.format(skill_data[2], attr_str)
    elif skill_type == 82:
        s.effect = "Hits for 100% ATK"
    elif skill_type == 83:
        effects = []
        for val in skill_data[2:]:
            c_skill = get_skill_from_id(val)
            if c_skill is not None:
                effects.append(c_skill.effect)
        effect_str = ', '.join(effects)
        s.effect = "Uses the following skills: {}".format(effect_str)
    elif skill_type == 84:
        attrs = get_attrs_from_shift(int(skill_data[2]))
        s.effect = "Changes all orbs to {}".format(', '.join(attrs))
    elif skill_type == 85:
        attrs = get_attrs_from_shift(int(skill_data[-1]))
        s.effect = "Hit for {}% ATK and changes all orbs to {}".format(skill_data[2], ', '.join(attrs))
    elif skill_type == 86:
        min_val = skill_data[2]
        max_val = skill_data[3]

        if min_val == max_val:
            heal_amount = '{}%'.format(min_val)
        else:
            heal_amount = '{}% to {}%'.format(min_val, max_val)

        s.effect = "Heals player for {} of team health".format(heal_amount)

    elif skill_type == 89:
        s.effect = "Delays skill cooldown by {} turn(s)".format(skill_data[2])
    elif skill_type == 90:
        s.effect = "Checks if the following cards are on your team: {}".format(', '.join(skill_data[2:]))
    elif skill_type == 92:
        attrs = get_attrs_from_shift(int(skill_data[2]))
        exclude = get_attrs_from_shift(int(skill_data[3]))
        s.effect = "Changes all orbs except {} to {}".format(', '.join(attrs), ', '.join(exclude))

    elif skill_type == 93:
        s.effect = "Final Fantasy animation"
    elif skill_type == 94:
        # this needs work
        attrs = get_attrs_from_shift(int(skill_data[2]))
        s.effect = "Locks {} orbs".format(', '.join(attrs))
    elif skill_type == 95:
        if len(skill_data) > 2:
            effect = get_skill_from_id(int(skill_data[2]))
            s.effect = "On death, do the following: {}".format(effect.effect if effect is not None else 'Unknown')

    elif skill_type == 97:
        min_orbs = int(skill_data[3])
        max_orbs = int(skill_data[4])
        if min_orbs == max_orbs:
            orbs = '{} orbs'.format(min_orbs)
        else:
            orbs = 'between {} and {} orbs'.format(min_orbs, max_orbs)
        s.effect = "Super-blinds {} for {} turns".format(orbs, skill_data[2])

    elif skill_type == 99:
        s.effect = "Tape binds the left most column of orbs"
    elif skill_type == 102:
        if len(skill_data) > 4:
            s.effect = "Hits for {}% ATK and randomly change {} orbs to bombs".format(skill_data[-1], skill_data[3])
        else:
            s.effect = "Randomly change {} orbs to bombs".format(skill_data[3])

    elif skill_type == 103:
        rows = get_orb_change_location(skill_data[3:-1])
        s.effect = "Changes orbs in the following rows to bombs: {}".format(rows)
    elif skill_type == 104:
        s.effect = "For {} turns, clouds view of orbs in the {} row, {} column with {} orb(s) in height, {} orb(s) in width".format(
            skill_data[-1], skill_data[2], skill_data[3], skill_data[4], skill_data[5])
    elif skill_type == 106:
        s.effect = "When HP is under {} , enemy's next turn changes by {}".format(skill_data[2], skill_data[-1])
    elif skill_type == 108:
        from_orbs = ', '.join(get_attrs_from_shift(int(skill_data[3])))
        to_orbs = ', '.join(get_attrs_from_shift(int(skill_data[-1])))

        s.effect = "Hit for {}% ATK, and change {} orb(s) to {} orb(s)".format(skill_data[2], from_orbs, to_orbs)
    elif skill_type == 118:
        types = get_types_from_shift(int(skill_data[2]))
        s.effect = "Reduces damage by {}% from {} type(s)".format(skill_data[-1], ', '.join(types))
    elif skill_type == 122:
        s.effect = "Enemy turn changes by {} turn(s) when {} enemy remains".format(skill_data[-1], skill_data[2])


def parse_skill(split_skill_data: list) -> EnemySkill:

    if len(split_skill_data) > 0:
        s = EnemySkill()

        s.skill_id = int(split_skill_data[0])

        name = split_skill_data[1]

        if 'なし' not in name or '*' not in name:

            curr_index = 2
            while curr_index < len(split_skill_data) and not split_skill_data[curr_index].isdigit():
                name += split_skill_data[curr_index]
                curr_index += 1

            s.name = name
            split_skill_data = split_skill_data[curr_index:]

            val = int(split_skill_data[1], 16)
            if val & 1:
                if not split_skill_data[2].isdigit():
                    message_str = ''
                    for item in split_skill_data[2:]:
                        if not item.isdigit():
                            message_str += item

                    s.effect = message_str

            else:
                make_effect(s.skill_type, s, split_skill_data)

        return s

skill_lookup_map = {}
parsed_skills = []


def parse_enemy_skills(data) -> [EnemySkill]:
    skills = data['enemy_skills'].split('\n')

    for skill in skills:
        split_skill_data = skill.split(',')
        if len(split_skill_data) > 0:
            if split_skill_data[0].isdigit():
                skill_lookup_map[split_skill_data[0]] = split_skill_data

    for skill in skills:
        split_skill_data = skill.split(',')

        if split_skill_data[0].isdigit():
            if len(split_skill_data) > 0:
                s = parse_skill(split_skill_data)
                parsed_skills.append(s)

    return parsed_skills
