from django.core.management.base import BaseCommand
import praw
from karmaleaderboard.models import RedditUser

import time


class Command(BaseCommand):
    help = 'Collects karma count for users in the PAD subreddit.'

    def handle(self, *args, **options):

        karmaCounts = {}

        reddit = praw.Reddit(client_id='EpY38Dgrh13atw',
                             client_secret='XaVpdm7mbCUz1zjsPcz5hWRZKVU',
                             user_agent='karma-calculator-hijackerjack')

        def addScore(post):
            if post.author not in karmaCounts.keys():
                karmaCounts[post.author] = post.score

            else:
                karmaCounts[post.author] += post.score

        def addCommentScore(comment):
            if comment is None:
                return

            addScore(comment)

            comment.replies.replace_more()

            for reply in comment.replies:
                addCommentScore(reply)

        for post in list(reddit.subreddit('puzzleanddragons').top(time_filter="day")):

            addScore(post)

            post.comments.replace_more()

            for comment in post.comments:
                addCommentScore(comment)

        karmaCounts["Deleted Users"] = karmaCounts[None]
        del karmaCounts[None]

        for person in karmaCounts.keys():

            if not RedditUser.objects.filter(author=person).exists():

                entry = RedditUser()
                entry.author = person
                entry.score = karmaCounts[person]
                entry.save()

            else:
                entry = RedditUser.objects.get(author=person)
                entry.score += karmaCounts[person]
                entry.save()

