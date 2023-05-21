import praw
from praw.models import MoreComments
import pandas as pd

reddit = praw.Reddit(
    client_id="ntkKZqDx0KMcF3mo1i-SCQ",
    client_secret="-SGJkpxOuMEQ881eERB9OELIICY2jw",
    user_agent="nba-sentiment/1.0 (by u/moneymichal)",
)

print(reddit.user.me())


def gather_more_comments(submission):
    top_level_comment_count = 0
    more_comments = []
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            more_comments.append(top_level_comment)
        else:
            top_level_comment_count += 1

    print(
        f"Comments: {top_level_comment_count}, MoreComments objects: {len(more_comments)}"
    )
    return more_comments


def get_comments(thread_id):
    submission = reddit.submission(thread_id)
    num_comments = submission.num_comments
    count_requests = 1

    more_comments = gather_more_comments(submission)

    while more_comments:
        more_comment = more_comments.pop()
        new_comments = more_comment.comments(update=False)
        count_requests += 1

        for comment in new_comments:
            if isinstance(comment, MoreComments) and comment.parent_id.startswith(
                "t1_"
            ):
                continue
            submission.comments._insert_comment(comment)

        submission.comments._comments.remove(more_comment)
        more_comments = gather_more_comments(submission)

    print(
        f"Done in {count_requests} requests. Of {num_comments}, top-level comments = {len(submission.comments)}"
    )

    return submission


def make_comments_csv(submission):
    comments = submission.comments
    columns = ["id", "body", "score", "utc", "parent_id"]
    data = []

    for comment in comments:
        data.append(
            [
                comment.id,
                comment.body,
                comment.score,
                comment.created_utc,
                comment.parent_id,
            ]
        )

    df = pd.DataFrame(data, columns=columns)
    filename = str(submission.id) + ".csv"
    df.to_csv(filename, index=False)

    print(f"finished creating {filename}")


def main():
    game_ids = ["1365zfw", "1384hu8", "13a5us2", "13can6x", "13e8sqq", "13g2qr3"]
    for id in game_ids:
        make_comments_csv(get_comments(id))


if __name__ == "__main__":
    main()
