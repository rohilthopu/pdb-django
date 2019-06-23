from rest_framework.views import APIView
from rest_framework.response import Response

from .models import GuerrillaDungeon


class GuerrillaList(APIView):
    def get(self, request):
        data = GuerrillaDungeon.objects.values()
        return Response(data)
