from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Dungeon, Floor, EncounterSet


class DungeonList(APIView):
    def get(self, request):
        data = Dungeon.objects.values()
        return Response(data)


class FloorList(APIView):
    def get(self, request):
        data = Floor.objects.values()
        return Response(data)


class EncounterList(APIView):
    def get(self, request):
        data = EncounterSet.objects.values()
        return Response(data)
