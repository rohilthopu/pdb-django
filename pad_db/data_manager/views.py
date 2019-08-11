from django.http import JsonResponse
from .search import query_es


def search(request, query):
    query_results = query_es(query)


    if len(query_results) == 1:
        return JsonResponse(query_results[0].to_dict(), json_dumps_params={'indent': 4})

    search_results = [result.to_dict() for result in query_results]

    return JsonResponse(search_results, safe=False, json_dumps_params={'indent': 4})
