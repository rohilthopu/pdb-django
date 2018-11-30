from django.core.management.base import BaseCommand
import praw
from karmaleaderboard.models import RedditUser

class Command(BaseCommand):
    help = 'Collects karma count for users in the PAD subreddit.'

    def handle(self, *args, **options):

        RedditUser.objects.all().delete()

        karmaCounts = {}

        reddit = praw.Reddit(client_id='EpY38Dgrh13atw',
                             client_secret='XaVpdm7mbCUz1zjsPcz5hWRZKVU',
                             user_agent='karma-calculator-hijackerjack')

        def addScore(post):
            if post.author not in karmaCounts.keys():
                karmaCounts[post.author] = post.score

            else:
                karmaCounts[post.author] += post.score

        for post in reddit.subreddit('puzzleanddragons').top(limit=10):

            addScore(post)

            post.comments.replace_more(limit=0)
            for comment in post.comments:
                addScore(comment)

        for person in karmaCounts.keys():



            entry = RedditUser()

            if person is None:
                entry.author = "Deleted User"
            else:
                entry.author = person

            entry.score = karmaCounts[person]
            entry.save()



