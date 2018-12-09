from django.shortcuts import render
from .models import RedditUser


# Create your views here.
def leaderboardView(request):
    template = 'karmaLeaderboard.html'

    users = RedditUser.objects.all()

    context = {'users': users}

    return render(request, template, context)
