from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Skill


class SkillList(APIView):
    def get(self, request):
        data = Skill.objects.exclude(name='').exclude(name="無し").exclude(skill_part_1_id=-1)\
            .values('name', 'description', 'skill_id', 'server')
        return Response(data)


class SkillObject(APIView):
    def get(self, request, skill_id):
        data = Skill.objects.filter(skill_id=skill_id).values().first()
        return Response(data)
