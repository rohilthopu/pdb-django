
OPERATORS = ['>=', '<=', '=', '>', '<']
INDICES = ['skills', 'monsters']
COLUMNS = ['CARD_ID', 'NAME']

ATTRIBUTE_ALIASES = {
    'hpmf': 'leader_skill.hp_mult_full',
    'atkmf': 'leader_skill.atk_mult_full',
    'rcvmf': 'leader_skill.rcv_mult_full',
    'hpm': 'leader_skill.hp_mult',
    'atkm': 'leader_skill.atk_mult',
    'rcvm': 'leader_skill.rcv_mult',
    'leader_shield': 'leader_skill.shield',
    'pair_shield': 'leader_skill.shield_full',
    'active_hpm': 'active_skill.hp_mult',
    'active_atkm': 'active_skill.atk_mult',
    'active_rcvm': 'active_skill.rcv_mult',
    'active_shield': 'active_skill.shield',
    'has_evomat': 'evolution_materials',
    'has_devomat': 'un_evolution_materials',
    'has_evomat_raw': 'evolution_materials_raw',
    'has_devomat_raw': 'un_evolution_materials_raw',
}

LEADER_SKILL_VALUES = {'leader_skill.hp_mult_full', 'leader_skill.rcv_mult_full', 'leader_skill.rcv_mult', 'leader_skill.shield_full',
                       'leader_skill.atk_mult', 'leader_skill.atk_mult_full', 'leader_skill.shield', 'leader_skill.hp_mult'}

ACTIVE_SKILL_VALUES = {'active_skill.atk_mult', 'active_skill.shield',
                       'active_skill.rcv_mult', 'active_skill.hp_mult'}

AWAKENINGS = {
    '': 0,
    'Enhanced HP': 1,
    'Enhanced Attack': 2,
    'Enhanced Heal': 3,
    'Reduce Fire Damage': 4,
    'Reduce Water Damage': 5,
    'Reduce Wood Damage': 6,
    'Reduce Light Damage': 7,
    'Reduce Dark Damage': 8,
    'Auto-Recover': 9,
    'Resistance-Bind': 10,
    'Resistance-Dark': 11,
    'Resistance-Jammers': 12,
    'Resistance-Poison': 13,
    'Enhanced Fire Orbs': 14,
    'Enhanced Water Orbs': 15,
    'Enhanced Wood Orbs': 16,
    'Enhanced Light Orbs': 17,
    'Enhanced Dark Orbs': 18,
    'Extend Time': 19,
    'Recover Bind': 20,
    'Skill Boost': 21,
    'Enhanced Fire Att.': 22,
    'Enhanced Water Att.': 23,
    'Enhanced Wood Att.': 24,
    'Enhanced Light Att.': 25,
    'Enhanced Dark Att.': 26,
    'Two-Pronged Attack': 27,
    'Resistance-Skill Bind': 28,
    'Enhanced Heal Orbs': 29,
    'Multi Boost': 30,
    'Dragon Killer': 31,
    'God Killer': 32,
    'Devil Killer': 33,
    'Machine Killer': 34,
    'Balanced Killer': 35,
    'Attacker Killer': 36,
    'Physical Killer': 37,
    'Healer Killer': 38,
    'Evolve Material Killer': 39,
    'Awaken Material Killer': 40,
    'Enhance Material Killer': 41,
    'Vendor Material Killer': 42,
    'Enhanced Combo': 43,
    'Guard Break': 44,
    'Additional Attack': 45,
    'Enhanced Team HP': 46,
    'Enhanced Team RCV': 47,
    'Damage Void Shield Penetration': 48,
    'Awoken Assist': 49,
    'Super Additional Attack': 50,
    'Skill Charge': 51,
    'Resistance-Bind＋': 52,
    'Resistance-Cloud': 54,
    'Extend Time＋': 53,
    'Resistance-Board Restrict': 55,
    'Skill Boost＋': 56,
    'Enhance when HP is above 80%': 57,
    'Enhance when HP is below 50%': 58,
    'L-Shape Damage Reduction': 59,
    'L-Shape Attack': 60,
    'Super Enhanced Combo': 61,
    'Combo Orb': 62,
    'Skill Voice': 63,
    'Dungeon Bonus': 64,
    'Reduced HP': 65,
    'Reduced Attack': 66,
    'Reduced RCV': 67,
}

AWAKENING_ALIASES = {
    '7c': 43,
    '10c': 61,
    'unbindable': 10,
    'unbindable+': 52,
    'autoheal': 9,
    'blind resist': 10,
    'jammer resist': 12,
    'poison resist': 13,
    'time extend': 19,
    'te': 19,
    'bind clear': 20,
    'sb': 21,
    'tpa': 27,
    'prong': 27,
    'skill bind resist': 28,
    'sbr': 28,
    'heal prong': 29,
    'fua': 45,
    'follow up attack': 45,
    'followup attack': 45,
    'team hp+': 46,
    'team rcv+': 46,
    'super fua': 50,
    'fua2': 50,
    'fua 2': 50,
    'vdp': 48,
    'dvp': 48,
    'void damage piercer': 48,
    'equip': 49,
    'time extend+': 53,
    'te+': 53,
    'tape resist': 55,
    'sb+': 56,
    'gt 80%': 57,
    'lt 50%': 58,
    'l unlock': 59,
    'l-unlock': 59,
    'l attack': 60,
    'l-attack': 60,
    'hp down': 65,
    'atk down': 66,
    'rcv down': 67,
    'poison resist+': 70,
    'jammer resist+': 71,
    'blind resist+': 72,
}