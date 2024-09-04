import praw, os
from datetime import datetime
from dotenv import load_dotenv

from analyzer import analysis, extract_ticker

# Load variables from env
load_dotenv()

# create instance of reddit
reddit = praw.Reddit(
    client_id="OlMydM-kjWVxaKFeXBrNuA",
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent="windows:genesis:v1 (by /u/ThisDudeHasNoLife )",
)


def grabSubInfo(subs):
    """Grabs basic info from given subreddits.
    
    Params:
    subs (list of subreddits)

    Returns:
    submissions (list of dicts/submissions)
    """

    submissions = []
    subreddits = ""

    # concatenate list of subs into one string (PRAW request format "sub1+sub2") 
    for subreddit in subs:
        subreddits += subreddit + "+"
    subreddits = subreddits[:-1]

    for submission in reddit.subreddit(subreddits).hot(limit=10):
        date = datetime.fromtimestamp(submission.created_utc)
        date = date.strftime("%Y-%m-%d %H:%M")
        submissions.append({"title" : submission.title,
                            "body" : submission.selftext,
                            "vote_ratio": submission.upvote_ratio,
                            "num_comments": submission.num_comments,
                            "date": date,
                            "tickers": extract_ticker(submission),
                            "sentiment": analysis(submission),
                            "link": submission.permalink})

    return submissions

def searchSubInfo(text):
    """Grabs basic info from given search query.
    
    Params:
    text (string)

    Returns:
    submissions (list of dicts/submissions)
    """

    submissions = []
    subreddits = ""

    for submission in reddit.subreddit("Stocks+StockMarket+Investing+ValueInvesting+Economics+Technology+Finance").search(text, "hot", limit=10):
        date = datetime.fromtimestamp(submission.created_utc)
        date = date.strftime("%Y-%m-%d %H:%M")
        submissions.append({"title" : submission.title,
                            "body" : submission.selftext,
                            "vote_ratio": submission.upvote_ratio,
                            "num_comments": submission.num_comments,
                            "date": date,
                            "tickers": extract_ticker(submission),
                            "sentiment": analysis(submission),
                            "link": submission.permalink})

    return submissions