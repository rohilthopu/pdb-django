from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Monster
from .serializers import MonsterSerializer


class MonsterList(APIView):
    def get(self, request):
        dungeons = Monster.objects.all()
        data = MonsterSerializer(dungeons, many=True).data
        return Response(data)
