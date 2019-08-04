from django.http import JsonResponse
from .search import query_es


def search(request, query):
    query_results = query_es(query)

    search_results = [result.to_dict() for result in query_results]
    return JsonResponse(search_results, safe=False, json_dumps_params={'indent': 4})
