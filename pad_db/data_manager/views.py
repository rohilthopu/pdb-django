from django.http import JsonResponse
from .documents import MonsterDocument, SkillDocument, DungeonDocument


def monster_search(request, query):
    results = MonsterDocument.search().filter('match', name=query)
    for r in results:
        print(r.name, r.card_id)

    return JsonResponse([{'name': r.name, 'card_id': r.card_id} for r in results], safe=False)


def dungeon_search(request, query):
    results = DungeonDocument.search().filter('match', name=query)
    for r in results:
        print(r.name, r.dungeon_id)

    return JsonResponse(results.to_dict())


def skill_search(request, query):
    results = SkillDocument.search().filter()
    for r in results:
        print(r.name, r.skill_id)
        print(r.description)
        print()

    return JsonResponse(results.to_dict())
