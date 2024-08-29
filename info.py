import praw
from datetime import datetime

# create instance of reddit
reddit = praw.Reddit(
    client_id="OlMydM-kjWVxaKFeXBrNuA",
    client_secret="2rdSeB0L-BVOd3e6NYUMEsRk0SugIw",
    user_agent="windows:genesis:v1 (by /u/ThisDudeHasNoLife )",
)


def grabSubInfo(subs):
    
    submissions = []
    subreddits = ""

    # concatenate list of subs into one string (PRAW request format "sub1+sub2") 
    for subreddit in subs:
        subreddits += subreddit + "+"
    subreddits = subreddits[:-1]

    for submission in reddit.subreddit(subreddits).hot(limit=25):
        date = datetime.fromtimestamp(submission.created_utc)
        date = date.strftime("%Y-%m-%d %H:%M")
        submissions.append({"title" : submission.title,
                            "vote_ratio": submission.upvote_ratio,
                            "num_comments": submission.num_comments,
                            "date": date,
                            "rel_tickers": getTickers(submission),
                            "sentiment": sentiment(submission)})

    return submissions

def getTickers(sub):


def sentiment(sub):
