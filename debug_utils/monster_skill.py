from skill_type_maps import SKILL_TYPE
from skill_parser import parse_skill_multiplier
from skill_parser import Multiplier
import re


def strip_colors(message: int) -> str:
    return re.sub(r'(?i)[$^][a-f0-9]{6}[$^]', '', message)


class MonsterSkill():
    """Leader/active skill info for a player-ownable monster."""

    def __init__(self, skill_id: int, raw: list):
        self.skill_id = int(skill_id)

        # Skill name text.
        self.name = str(raw[0])

        # Skill description text (may include formatting).
        self.description = str(raw[1])

        # Skill description text (no formatting).
        self.clean_description = strip_colors(
            self.description).replace('\n', ' ').replace('^p', '')

        # Encodes the type of skill (requires parsing other_fields).
        self.skill_type = int(raw[2])

        # New field. Describes the idea that a skill falls into
        self.skill_class = SKILL_TYPE[self.skill_type]

        # If an active skill, number of levels to max.
        levels = int(raw[3])
        self.levels = levels if levels else None

        # If an active skill, maximum cooldown.
        self.turn_max = int(raw[4]) if self.levels else None

        # If an active skill, minimum cooldown.
        self.turn_min = self.turn_max - (self.levels - 1) if levels else None

        # Unknown field.
        self.unknown_005 = raw[5]

        # Fields used in coordination with skill_type.
        self.other_fields = raw[6:]

        # NEW FIELDS. The skills that a skill links to if it has multiple
        # clauses/conditions for activation
        self.skill_part_1_id = None
        self.skill_part_2_id = None
        self.skill_part_3_id = None

        if self.skill_type == 116 or self.skill_type == 138:
            self.skill_part_1_id = self.other_fields[0]
            self.skill_part_2_id = self.other_fields[1]
            if len(self.other_fields) == 3:
                self.skill_part_3_id = self.other_fields[2]

        try:
            multipliers = parse_skill_multiplier(
                int(raw[2]), self.other_fields, len(self.other_fields))
        except Exception as e:
            print('skill parsing failed for', raw[2], 'with exception:', e)
            multipliers = Multiplier()

        self.hp_mult = multipliers.hp
        self.atk_mult = multipliers.atk
        self.rcv_mult = multipliers.rcv

        # This gives you the shield as a percent rather than a fraction
        self.shield = multipliers.shield * 100

