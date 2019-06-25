from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Dungeon, Floor


class DungeonList(APIView):
    def get(self, request):
        data = Dungeon.objects.exclude(name__contains='*').values('name', 'dungeon_id', 'image_id', 'server', 'floor_count')
        return Response(data)


class DungeonObject(APIView):
    def get(self, request, dungeon_id):
        data = Dungeon.objects.filter(dungeon_id=dungeon_id).values().first()
        return Response(data)


class AllFloorsList(APIView):
    def get(self, request):
        data = Floor.objects.values('dungeon_id', 'image_id', 'name')
        return Response(data)


class FloorList(APIView):
    def get(self, request, dungeon_id):
        data = Floor.objects.filter(dungeon_id=dungeon_id).values('dungeon_id', 'image_id', 'name', 'stamina', 'waves')
        return Response(data)


class FloorObject(APIView):
    def get(self, request, dungeon_id, floor_number):
        data = Floor.objects.filter(dungeon_id=dungeon_id, floor_number=floor_number).values().first()
        return Response(data)
