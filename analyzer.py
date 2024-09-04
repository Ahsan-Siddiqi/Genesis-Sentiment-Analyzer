from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch.nn.functional as F

from ticker_extraction import grabCompany, grabTicker, companyToTicker

# model from https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis
tokenizer = AutoTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
model = AutoModelForSequenceClassification.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

def analyze_sentiment(text):
    """Analyses Sentiment From Financial Text Using NER"""

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

    outputs = model(**inputs)

    probabilities = F.softmax(outputs.logits, dim=1).detach().numpy()[0]
    
    sentiments = ["Negative", "Neutral", "Positive"]
    sentiment_percentage = {sentiment: round(prob * 100, 2) for sentiment, prob in zip(sentiments, probabilities)}

    total_percentage = sum(sentiment_percentage.values())
    if not (99.99 <= total_percentage <= 100.01):
        return -1

    # model wasn't trained for financial lingo :( 
    if "short" in text.lower() or "downgrade" in text.lower():
        sentiment_percentage["Negative"] += 10
        sentiment_percentage["Positive"] -= 10 

    total = sum(sentiment_percentage.values())
    sentiment_percentage = {k: round((v / total) * 100, 2) for k, v in sentiment_percentage.items()}

    return sentiment_percentage

def analysis(sub):
    """Analyses Sentiment From Submissions"""

    if not sub.selftext:
        return analyze_sentiment(sub.title)
    else:
        return analyze_sentiment(sub.selftext)

def extract_ticker(sub):
    """Parses Ticker From Submissions"""

    tickers = set()

    if not sub.selftext:
        tickers.update(grabTicker(sub.title))
        tickers.update(companyToTicker(grabCompany(sub.title)))
    else:
        tickers.update(grabTicker(sub.selftext))
        tickers.update(companyToTicker(grabCompany(sub.selftext)))
    
    if not tickers:
        return {"SPX", "INDU", "NDX"}

    return tickers
