from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Dungeon


class DungeonList(APIView):
    def get(self, request):
        data = Dungeon.objects.values()
        return Response(data)
