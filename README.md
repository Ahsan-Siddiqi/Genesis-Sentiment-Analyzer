![Alt Text](Readme/logo1.png)

# Genesis Sentiment Analyzer
Genesis is a sentiment analysis tool that analyses submissions from handpicked subreddits using natural language processing.

[Progress](#progress) | [Models and API](#models-and-api) | [Development](#development) 

<br>

## Progress

### Overview
Alpha Release Overview: [Youtube](https://www.youtube.com/watch?v=UEvtx_zl0Gg&t=15)

### Future Release/Features underway
* Redo ENTIRE frontend with dedicated framework (react or vue)   
* Refactor backend to create endpoints using flask
* New features
  * Implement user accounts
    * Custom Subreddit feeds
    * Saved submissions
    * Portfolio
  * Implement overall market sentiment with timeframes
  * Implement sector sentiment
  * Implement in-depth submission analysis page
* Fix search performance and bugs
* More integration with finnhub (or other possible alternatives)

<br>

## Models and API
* https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis 
* https://huggingface.co/ProsusAI/finbert
* https://finnhub.io/docs/api

<br>

## Development
We are in alpha testing. The alpha release will contain bugs and is not the complete form of this webapp.

### Start
<pre>
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt OR pip install -r requirements_full.txt
  flask --debug run
</pre>

### API keys
Get your finnhub API key from [finnhub](https://finnhub.io/dashboard)
<br>
Get your reddit API key by following these steps: <br>https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
<br><br>
You need: 
* client_id
* client_secret
* user_agent

the client_id and user agent go in `info.py`
<pre>
  reddit = praw.Reddit(
    client_id=" ", // <--------------------------------------HERE
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=" " // <-------------------------------------------------HERE,
  )
</pre>

the API keys go in a .env file which you need to create
<pre>
  FINNHUB_API_KEY= // <-------------------------------------------------HERE
  REDDIT_CLIENT_SECRET= // <-------------------------------------------------HERE
</pre>
