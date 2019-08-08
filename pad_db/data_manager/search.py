from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from prettytable import PrettyTable

# this just allows me to run the script outside of the djano env for testing
try:
    from .maps import AWAKENINGS
except:
    from maps import AWAKENINGS

client = Elasticsearch('https://elastic.pad-db.com')

operators = ['>=', '<=', '=', '>', '<']
int_attributes = ['awakenings', 'evolutions']
indices = ['skills', 'monsters']
COLUMNS = ['CARD_ID', 'NAME']

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

ATTRIBUTE_ALIASES = {
    'hpmf': 'leader_skill.hp_mult_full',
    'atkmf': 'leader_skill.atk_mult_full',
    'rcvmf': 'leader_skill.rcv_mult_full',
    'hpm': 'leader_skill.hp_mult',
    'atkm': 'leader_skill.atk_mult',
    'rcvm': 'leader_skill.rcv_mult',
    'leader shield': 'leader_skill.shield',
    'pair shield': 'leader_skill.shield_full',
    'active_hpm': 'active_skill.hp_mult',
    'active_atkm': 'active_skill.atk_mult',
    'active_rcvm': 'active_skill.rcv_mult',
    'active_shield': 'active_skill.shield',
    'has_evomat': 'evolution_materials',
    'has_devomat': 'un_evolution_materials',
    'has_evomat_raw': 'evolution_materials_raw',
    'has_devomat_raw': 'un_evolution_materials_raw',
}


def update_awakening_map():
    AWAKENINGS.update(AWAKENING_ALIASES)
    AWAKENINGS.update({key.upper(): val for key, val in AWAKENINGS.items()})
    AWAKENINGS.update({key.lower(): val for key, val in AWAKENINGS.items()})


def show_results(hits):
    table = PrettyTable()
    table.field_names = ['CARD_ID', 'NAME']
    for hit in hits:
        table.add_row([hit.card_id, hit.name])
    print(table)


def match_monster_from_name(monster_name: str):
    s = Search(using=client, index="monsters").query('match', name=monster_name)
    eq_tokens = monster_name.split(' ')
    for tok in eq_tokens:
        s = s.query("match", name=tok.strip())
    s = s[0:s.count()]
    s = s.execute()
    return s.hits


def match_monster_from_hit(hit, monster_name):
    s = Search(using=client, index="monsters")
    if monster_name is not None:
        eq_tokens = monster_name.split(' ')
        for tok in eq_tokens:
            s = s.query("match", name=tok.strip())

    if hit.skill_type == 'active':
        s = s.filter("term", **{'active_skill_id': hit.skill_id})
    elif hit.skill_type == 'leader':
        s = s.filter("term", **{'leader_skill_id': hit.skill_id})

    s = s[0:s.count()]
    s = s.execute()
    return s.hits


def filter_by_query_tokens(es_search: Search, attribute: str, tokens: [], q_type: str):
    for token in tokens:
        body = {attribute: token}
        print('Filtering by token : {}'.format(token))
        es_search = es_search.filter(q_type, **body)
    return es_search


def query_by_terms_list(es_search: Search, attribute: str, values: []):
    body = {attribute: values}
    print('Body generated: {}'.format(body))
    return es_search.filter('terms', **body)


def query_by_script(es_search: Search, body: {}):
    return es_search.filter('script', **body)


def query_by_awakenings(es_search: Search, attribute: str, value: str):
    print('Matched raw values for {}'.format(attribute))
    awakenings = [val.strip() for val in value.strip().split(',')]
    print('Requested awakenings: {}'.format(awakenings))
    for awakening in awakenings:
        # see if there is a count requested
        awk_parts = awakening.split('x')
        # reset the pure awakening str value
        awakening = awk_parts[0].strip()
        # this would be the count requested i.e. x2, x3 etc

        if awakening in AWAKENINGS:
            # raw_awakenings.append(AWAKENINGS[awakening])
            raw_awakening = AWAKENINGS[awakening]
            print('Found raw awakening: {} for {}'.format(raw_awakening, awakening))
            if len(awk_parts) > 1:
                count = int(awk_parts[1].strip())
                atr_label = attribute + '_raw'

                script = \
                    """
                    int total = 0; 
                    for (int i = 0; i < doc[\'%s\'].length; ++i) { 
                        if (doc[\'%s\'][i] == %i) { 
                            total += 1;
                        } 
                    }    
                    return total == %i;
                    """ % (atr_label, atr_label, raw_awakening, count)

                print('Found request of {} {}'.format(count, attribute))
                print('Script : {}'.format(script))
                body = {'script': {'inline': script, 'lang': 'painless'}}
                es_search = query_by_script(es_search, body)

            else:
                es_search = query_by_terms_list(es_search, attribute + '_raw', [raw_awakening])
        else:
            print('Invalid awakening found: {}'.format(awakening))

    return es_search


def query_evolves_into(es_search: Search, value: str):
    print('Matched Evolves Into Query')
    evolutions = []
    for val in value.strip().split(','):
        monsters = match_monster_from_name(val.strip())
        evolutions.extend([monster.ancestor_id for monster in monsters])
    print('Matched {} to {}'.format(value, evolutions))
    if len(evolutions) > 0:
        return query_by_terms_list(es_search, 'card_id', evolutions)
    return es_search


def query_evolves_from(es_search: Search, value: str):
    print('Matched Evolves From Query')
    evolutions = []
    for val in value.strip().split(','):
        monsters = match_monster_from_name(val.strip())
        for monster in monsters:
            if 'evolution_list' in monster.to_dict():
                evolutions.extend(monster.evolution_list)
    print('Matched {} to {}'.format(value, evolutions))
    if len(evolutions) > 0:
        return query_by_terms_list(es_search, 'card_id', evolutions)
    return es_search


def query_evolution_lists(es_search: Search, attribute: str, value: str):
    print('Matched {} Query'.format(attribute))
    materials = []
    for val in value.strip().split(','):
        monsters = match_monster_from_name(val.strip())
        materials.extend([monster.card_id for monster in monsters])
    print('Found materials : {} '.format(materials))
    if len(materials) > 0:
        for material in materials:
            es_search = query_by_terms_list(es_search, attribute + '_raw', [material])
    return es_search


def query_evolution_lists_raw(es_search: Search, attribute: str, value: str):
    print('Matched {} Query'.format(attribute))
    print('Found materials : {} '.format(value))
    for val in value.strip().split(','):
        es_search = query_by_terms_list(es_search, attribute, [val])
    return es_search


def query_monster_types(es_search: Search, value: str):
    print('Matched TYPE query')
    monster_types = [val.strip() for val in value.strip().split(',')]
    print('Requested types: {}'.format(monster_types))
    for monster_type in monster_types:
        es_search = query_by_terms_list(es_search, 'type', [monster_type])
    return es_search


def query_equals(es_search: Search, attribute: str, value: str):
    print('Matched EQ')
    if attribute == 'awakenings' or attribute == 'super_awakenings':
        return query_by_awakenings(es_search, attribute, value)
    elif attribute == 'evolves_into':
        return query_evolves_into(es_search, value)
    elif attribute == 'evolves_from':
        return query_evolves_from(es_search, value)
    elif attribute == 'type':
        return query_monster_types(es_search, value)
    elif attribute == 'evolution_materials':
        if 'raw' in attribute:
            return query_evolution_lists_raw(es_search, attribute, value)
        return query_evolution_lists(es_search, attribute, value)

    body = {attribute: value.strip()}

    # eq_tokens = value.strip().split(' ')
    # for tok in eq_tokens:
    #     body = {attribute: tok.strip()}
    #     print('Body generated: {}'.format(body))
    #     es_search = es_search.filter('match', **body)
    return es_search.filter('match', **body)


def query_less_than(es_search: Search, operator: str, attribute: str, value: str):
    if '=' in operator:
        body = {attribute: {'lte': value}}
        print('Matched LTE')
        print('Body generated: {}'.format(body))
        return es_search.filter('range', **body)

    body = {attribute: {'lt': value}}
    print('Matched LT')
    print('Body generated: {}'.format(body))
    return es_search.filter('range', **body)


def query_greater_than(es_search: Search, operator: str, attribute: str, value: str):
    if '=' in operator:
        body = {attribute: {'gte': value}}
        print('Matched GTE')
        print('Body generated: {}'.format(body))
        return es_search.filter('range', **body)

    body = {attribute: {'gt': value}}
    print('Matched GT')
    print('Body generated: {}'.format(body))
    return es_search.filter('range', **body)


def query_name(es_search: Search, query_part: str):
    body = {}
    eq_tokens = query_part.strip().split(' ')
    for tok in eq_tokens:
        body['name'] = tok.strip()
        print('Body generated: {}'.format(body))
        es_search = es_search.query('match', **body)
    return es_search


def get_operator(query_part: str):
    for operator in operators:
        if operator in query_part:
            return operator
    return None


def analyze_query_part(es_search: Search, query_part: str):
    # if len(query_part) > 1:
    operator = get_operator(query_part)
    if operator is not None:
        tokens = query_part.split(operator)
        if len(tokens) > 1:
            attribute = tokens[0].strip().replace(' ', '_')
            value = tokens[1].strip()

            # if attribute not in ['evolves_into', 'awakenings', 'card_id', 'name']:
            #     COLUMNS.append(attribute.upper())
            #     VALUES.append(attribute)

            if attribute in ATTRIBUTE_ALIASES:
                attribute = ATTRIBUTE_ALIASES[attribute]

            print('Attribute: {}, Value: {}'.format(attribute, value))

            if '>' in operator:
                return query_greater_than(es_search, operator, attribute, value)
            elif '<' in operator:
                return query_less_than(es_search, operator, attribute, value)
            elif operator == '=':
                return query_equals(es_search, attribute, value)
    else:
        # assume that the user is looking for the name of the item
        print('Assuming NAME query: {}'.format(query_part))
        return query_name(es_search, query_part)


def query(index: str, raw_query: str):
    print('Removing whitespace..')
    raw_query_parts = raw_query.strip().split(' and ')
    print('Raw query parts: {}'.format(raw_query_parts))
    print()
    print('Creating search object connection')
    es_search = Search(using=client, index=index)

    monster_name = None
    print('Splitting up raw query')
    print()
    for query_part in raw_query_parts:
        print('Processing query part: {}'.format(query_part))
        es_search = analyze_query_part(es_search, query_part)
        print()

    print('Executing search...')
    print()
    es_search = es_search[0:es_search.count()]
    results = es_search.execute()

    if index == 'skills':
        monsters = []
        for hit in results.hits:
            monsters.extend(match_monster_from_hit(hit, monster_name))
        return monsters

    return results.hits


def query_es(query_str: str):
    update_awakening_map()
    # # index = input('Enter an index: ')
    # raw_query = input('Enter a query to filter data: ')
    index = 'monsters'
    raw_query = query_str
    # raw_query = 'awakenings = healer killer, balanced killer'

    if index in indices:
        print()
        print('Searching {} index'.format(index.upper()))
        print('Desired index: {}'.format(index))
        print('Input query: {}'.format(raw_query))
        print()

        raw_query = raw_query.split(' || ')
        query_results = []
        for rq in raw_query:
            query_results.extend(q for q in query(index, rq) if q not in query_results)

        print('FOUND {} ITEMS'.format(len(query_results)))
        print()
        show_results(query_results)
        print()
        return query_results

    print('Invalid Index requested: {}'.format(index.upper()))
    return []


def test_raw_query():
    update_awakening_map()
    # index = input('Enter an index: ')
    # raw_query = input('Enter a query to filter data: ')
    index = 'monsters'
    raw_query = 'has evomat = machine athena gem'

    if index in indices:
        print()
        print('Searching {} index'.format(index.upper()))
        print('Desired index: {}'.format(index))
        print('Input query: {}'.format(raw_query))
        print()

        raw_query = raw_query.split(' || ')
        query_results = []
        for rq in raw_query:
            query_results.extend(q for q in query(index, rq) if q not in query_results)

        print('FOUND {} ITEMS'.format(len(query_results)))
        print()
        show_results(query_results)
        print()
    else:
        print('Invalid Index requested: {}'.format(index.upper()))


if __name__ == "__main__":
    test_raw_query()
