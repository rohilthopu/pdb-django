from rest_framework.views import APIView
from rest_framework.response import Response

from .models import RedditUser


class LeaderboardList(APIView):
    def get(self, request):
        data = RedditUser.objects.values()
        return Response(data)


