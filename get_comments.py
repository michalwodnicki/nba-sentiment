import praw
from praw.models import MoreComments
import pandas as pd
import os
from config import CLIENT_ID, CLIENT_SECRET, USER_AGENT

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
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


def make_comments_csv(submission, folderName):
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
    outputFolder = f"data/{folderName}"
    os.makedirs(outputFolder, exist_ok=True)
    output_path = os.path.join(outputFolder, filename)
    df.to_csv(output_path, index=False)

    print(f"finished creating {filename}")


def main():
    game_ids = [
        "13khtbi",
        "13mbddv",
        "13o9v3a",
        "13q4i9d",
        "13rww5n",
        "13tlgsh",
        "13va0qi",
    ]
    for id in game_ids:
        make_comments_csv(get_comments(id), "MIAvBOS")


if __name__ == "__main__":
    main()
