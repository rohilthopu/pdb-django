from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from prettytable import PrettyTable
import os

# this just allows me to run the script outside of the djano env for testing
try:
    from .constants import AWAKENINGS, AWAKENING_ALIASES, ATTRIBUTE_ALIASES, LEADER_SKILL_VALUES, ACTIVE_SKILL_VALUES, \
        OPERATORS, COLUMNS, INDICES
except:
    from constants import AWAKENINGS, AWAKENING_ALIASES, ATTRIBUTE_ALIASES, LEADER_SKILL_VALUES, ACTIVE_SKILL_VALUES, \
        OPERATORS, COLUMNS, INDICES

client = Elasticsearch(os.environ.get('ELASTIC_CLIENT'))


def update_awakening_map():
    AWAKENINGS.update(AWAKENING_ALIASES)
    AWAKENINGS.update({key.upper(): val for key, val in AWAKENINGS.items()})
    AWAKENINGS.update({key.lower(): val for key, val in AWAKENINGS.items()})


def show_results(index: str, hits):
    table = PrettyTable()

    if index == 'skills':
        table.field_names = ['SKILL_ID', 'NAME']
        for hit in hits:
            table.add_row([hit.skill_id, hit.name])
    elif index == 'monsters':
        table.field_names = ['CARD_ID', 'NAME']
        for hit in hits:
            table.add_row([hit.card_id, hit.name])
    print(table)


def query_name(es_search: Search, query_part: str):
    body = {}
    eq_tokens = query_part.strip().split(' ')
    for tok in eq_tokens:
        body['name'] = tok.strip()
        print('Body generated: {}'.format(body))
        es_search = es_search.query('match', **body)
    return es_search


def match_monster_from_name(monster_name: str):
    s = Search(using=client, index="monsters")
    s = query_name(s, monster_name)
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
            print('Found raw awakening: {} for {}'.format(
                raw_awakening, awakening))
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
                es_search = query_by_terms_list(
                    es_search, attribute + '_raw', [raw_awakening])
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
                evolutions.extend(
                    [evo.card_id for evo in monster.evolution_list])
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
        es_search = query_by_terms_list(
            es_search, attribute + '_raw', materials)
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
    elif attribute == 'name':
        return query_name(es_search, value)

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


def get_operator(query_part: str):
    for operator in OPERATORS:
        if operator in query_part:
            return operator
    return None


def query_by_operator(es_search: Search, operator: str, attribute: str, value: str):
    """a function that chains a query based on a logical operator
    
    Arguments:
        es_search {Search} -- ES Search object
        operator {str} -- a logical operator
        attribute {str} -- object property being queried
        value {str} -- the raw value used to filter
    
    Returns:
        Search object -- passes back a modified Search object with new filters
    """
    # if len(query_part) > 1:
    print('Attribute: {}, Value: {}'.format(attribute, value))

    if '>' in operator:
        return query_greater_than(es_search, operator, attribute, value)
    elif '<' in operator:
        return query_less_than(es_search, operator, attribute, value)
    elif operator == '=':
        return query_equals(es_search, attribute, value)


def query_by_skill_attribute(skill_search: Search, operator: str, attribute: str, value: str):
    # and get the results for that individual item which i use to filter down the current monster index query values
    # this is a hack to get the actual attribute that we are querying from the skills index object
    # example : leader_skill.hp_mult_full -> hp_mult_full
    attribute = attribute.split('.')[-1]
    skill_search = query_by_operator(skill_search, operator, attribute, value)
    skill_search = skill_search[0:skill_search.count()]
    skill_search_results = skill_search.execute()
    return [hit.skill_id for hit in skill_search_results.hits]


def analyze_query_part(es_search: Search, query_part: str):
    operator = get_operator(query_part)
    if operator is not None:

        # atkmf >= 900 -> [atkmf, 900]
        tokens = query_part.split(operator)

        # this is to avoid cases where someone enters a broken query
        # example : atkmf >=
        # since this would lead to querying an empty value against atkmf
        if len(tokens) > 1:
            # this modifies an attribute as follows:
            # sub attribute id -> sub_attribute_id 
            # to query by the exact attribute stored in the index
            attribute = tokens[0].strip().replace(' ', '_').lower()

            # this gets the raw str value for whatever is being searched and removes trailing whitespace
            # i.e. ' 900 ' -> '900'
            # relies on elastic to correctly cast to the right type of value on query execution
            # holds up for now
            value = tokens[1].strip()

            # gets back the literal value for a given alias
            if attribute in ATTRIBUTE_ALIASES:
                attribute = ATTRIBUTE_ALIASES[attribute]

            # handle the case that the user searches for a leader skill alias based filter
            # this creates a new search object specifically to search the Skills index
            if attribute in LEADER_SKILL_VALUES:
                print('Found a leader skill query')
                skill_search = Search(using=client, index="skills").filter('term', **{'skill_type': 'leader'})
                skills = query_by_skill_attribute(skill_search, operator, attribute, value)
                return query_by_terms_list(es_search, 'leader_skill_id', skills)

            # handle the case where a user alias or literal was an active skill element
            elif attribute in ACTIVE_SKILL_VALUES:
                print('Found an active skill query')
                skill_search = Search(using=client, index="skills").filter('term', **{'skill_type': 'active'})
                skills = query_by_skill_attribute(skill_search, operator, attribute, value)
                return query_by_terms_list(es_search, 'active_skill_id', skills)

            # run a normal query filter in the monster index
            return query_by_operator(es_search, operator, attribute, value)

    # assume that the user is looking for the name of the item
    print('Assuming NAME query: {}'.format(query_part))
    return query_name(es_search, query_part)


def query(index: str, raw_query: str):
    """ElasticSearch query base method
    
    Arguments:
        index {str} -- an available elasticsearch index
        raw_query {str} -- the full-length raw query from the request
    
    Returns:
        [hits] -- a list of hits that match the users query in any way
    """
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

    return results.hits


def query_es(index: str, query_str: str):
    """a function that queries an ES index
    
    Arguments:
        query_str {str} -- a full-length query from an http request to django
    
    Returns:
        [hits] -- a set of hits from the es query
    """

    if index not in INDICES:
        return []

    update_awakening_map()

    # default center searches around monsters
    # this might change in the future
    index = index

    # input query from django request string
    raw_query = query_str

    # make sure the index exists (if i ever allow non monster centered queries)
    print()
    print('Searching {} index'.format(index.upper()))
    print('Desired index: {}'.format(index))
    print('Input query: {}'.format(raw_query))
    print()

    # break by logical OR
    # combines two query sets together and spits back the results.
    # not sure why anyone would use this tbh
    raw_query = raw_query.split(' || ')
    query_results = []
    for rq in raw_query:
        query_results.extend(q for q in query(
            index, rq) if q not in query_results)

    print('FOUND {} ITEMS'.format(len(query_results)))
    print()
    show_results(index, query_results)
    print()
    return query_results


def test_raw_query():
    update_awakening_map()
    raw_query = input('Enter a query to filter data: ')
    index = 'monsters'
    # raw_query = 'has evomat = machine athena gem'

    if index in INDICES:
        print()
        print('Searching {} index'.format(index.upper()))
        print('Desired index: {}'.format(index))
        print('Input query: {}'.format(raw_query))
        print()

        raw_query = raw_query.split(' || ')
        query_results = []
        for rq in raw_query:
            query_results.extend(q for q in query(
                index, rq) if q not in query_results)

        print('FOUND {} ITEMS'.format(len(query_results)))
        print()
        show_results(index, query_results)
        print()
    else:
        print('Invalid Index requested: {}'.format(index.upper()))


if __name__ == "__main__":
    test_raw_query()
