from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Monster, Skill, EnemySkill


class MonsterList(APIView):
    def get(self, request):
        data = Monster.objects.values('card_id')
        return Response(data)


class MonsterObject(APIView):
    def get(self, request, card_id):
        data = Monster.objects.filter(card_id=card_id).values()
        return Response(data)



class SkillList(APIView):
    def get(self, request):
        data = Skill.objects.values()
        return Response(data)


class EnemySkillList(APIView):
    def get(self, request):
        data = EnemySkill.objects.values()
        return Response(data)
