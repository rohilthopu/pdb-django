from django.http import JsonResponse
from .search import get_raw_query


def search(request, query):
    query_results = get_raw_query(query)

    search_results = [result.to_dict() for result in query_results]
    return JsonResponse(search_results, safe=False, json_dumps_params={'indent': 4})
