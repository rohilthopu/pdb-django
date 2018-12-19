from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import GuerrillaDungeon
from .serializers import GuerillaSerializer


class GuerrillaList(APIView):
    def get(self, request):
        dungeons = GuerrillaDungeon.objects.all()
        data = GuerillaSerializer(dungeons, many=True).data
        return Response(data)
