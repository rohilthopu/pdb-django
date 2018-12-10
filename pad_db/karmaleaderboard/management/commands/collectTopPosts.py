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
            if str(post.author) not in karmaCounts.keys():
                karmaCounts[str(post.author)] = post.score

            else:
                karmaCounts[str(post.author)] += post.score

        def addCommentScore(comment):
            if comment is None:
                return

            addScore(comment)

            comment.replies.replace_more()
            for reply in comment.replies:
                addCommentScore(reply)

        for post in reddit.subreddit('puzzleanddragons').top(limit=250):

            print("Collect karma for:", post.title)

            addScore(post)

            post.comments.replace_more()

            for comment in post.comments:
                addCommentScore(comment)

        if "None" in karmaCounts:
            karmaCounts["Deleted Users"] = karmaCounts["None"]
            del karmaCounts["None"]

        print()
        print("Storing new users....")
        print()

        for person in karmaCounts.keys():
            entry = RedditUser()
            entry.author = person
            entry.score = karmaCounts[person]
            entry.save()
