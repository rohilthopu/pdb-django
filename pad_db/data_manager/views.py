from django.http import JsonResponse
from django.shortcuts import redirect
from .search import query_es


def search(request, index, query):
    query_results = query_es(index, query)
    search_results = [result.to_dict() for result in query_results]
    return JsonResponse(search_results, safe=False, json_dumps_params={'indent': 4})


def get_monster_by_id(request, card_id):
    return redirect('/search/monsters/card_id={}'.format(card_id))


def get_skill_by_id(request, skill_id):
    return redirect('/search/skills/skill_id={}'.format(skill_id))
