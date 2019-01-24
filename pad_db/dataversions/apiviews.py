from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Version


class VersionList(APIView):
    def get(self, request):
        data = Version.objects.values()
        return Response(data)

