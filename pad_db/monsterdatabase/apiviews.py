from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Monster, Skill
from .serializers import MonsterSerializer, SkillSerializer


class MonsterList(APIView):
    def get(self, request):
        dungeons = Monster.objects.all()
        data = MonsterSerializer(dungeons, many=True).data
        return Response(data)


class SkillList(APIView):
    def get(self, request):
        dungeons = Skill.objects.all()
        data = SkillSerializer(dungeons, many=True).data
        return Response(data)
