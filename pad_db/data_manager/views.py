from django.http import JsonResponse
from django.shortcuts import redirect
from .search import query_es

list_params = ['awakenings_raw', 'awakenings', 'super_awakenings_raw', 'super_awakenings', 'evolution_list',
               'evolution_materials', 'evolution_materials_raw', 'un_evolution_materials', 'un_evolution_materials_raw']


def search(request, index, query):
    query_results = query_es(index, query)

    if len(query_results) == 1:
        final_results = query_results[0].to_dict()
        if index == 'monsters':
            fill_missing_values(final_results)
        return JsonResponse(query_results[0].to_dict(), json_dumps_params={'indent': 4})

    search_results = [result.to_dict() for result in query_results]
    if index == 'monsters':
        for result in search_results:
            fill_missing_values(result)

    return JsonResponse(search_results, safe=False, json_dumps_params={'indent': 4})


def fill_missing_values(query_result: dict):
    for param in list_params:
        if param not in query_result:
            query_result[param] = []


def get_monster_by_id(request, card_id):
    return redirect('/search/monsters/card_id={}'.format(card_id))


def get_skill_by_id(request, skill_id):
    return redirect('/search/skills/skill_id={}'.format(skill_id))
