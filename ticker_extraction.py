from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import re, requests, os

# Load variables from env
load_dotenv()

# Setup finnhub client
finnhub_api_key = os.getenv('FINNHUB_API_KEY')
base_url = "https://finnhub.io/api/v1/"

# Model from https://huggingface.co/dslim/bert-base-NER
# Load NER model and tokenizer for company names
model_name = "dslim/bert-base-NER"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

# # Model from https://huggingface.co/Jean-Baptiste/roberta-ticker
# # Load NER model and tokenizer for tickers
# ticker_tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/roberta-ticker")
# ticker_model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/roberta-ticker") 

# ticker_ner = pipeline('ner', model=ticker_model, tokenizer=ticker_tokenizer, aggregation_strategy="simple")

common_financial_abbreviations = {
    "EPS", "EBITDA", "P/E", "D/E", "ROI", "ROE", "ROA", "CAGR", "FIFO", "LIFO", "DCF", "NAV",
    "IPO", "ETF", "NAV", "ATM", "FD", "CD", "MBS", "REIT", "AUM", "NAV", "FY", "Q1", "Q2", "Q3", 
    "Q4", "EPS", "PEG", "DCF", "OPEX", "CAPEX", "MACD", "RSI", "GDP", "CPI", "PPI", "PMI", "MOM", 
    "YOY", "MBS", "IPO", "SEC", "FDIC", "OPEC", "FOMC", "TARP", "GMP", "HR", "CEO", "CFO", "COO", 
    "IR", "IRA", "ETF", "HFT", "IPO", "ESG", "EV", "FCF", "GAAP", "KPI", "LIBOR", "M&A", "NAV", 
    "PM", "I", "EPS", "GDP", "APR", "FD", "CD", "ADR", "AGM", "YTM", "MoM", "EMH", "NPV", 
    "P&L", "PV", "FV", "WACC", "PMT", "SEC", "FCA", "FD", "IPO", "IRR", "RSU", "KYC", "AML", 
    "AML", "CFD", "DMA", "DY", "ETF", "FX", "MOM", "YTD", "MoM", "PB", "PEG", "REIT", "SMA", 
    "SIPC", "SG&A", "SOX", "TCA", "TTM", "VWAP", "WTI", "YTM", "roth", "VP", "A", "AI", "US"
}

 
def grabCompany(text):
    """Parses Company Names Using NER 

    Parameters:
    text (str)

    Returns: 
    company_names (list)
    """
    ner_results = ner_pipeline(text)

    # Combine tokens to form full entity names
    entities = []
    current_entity = ""
    current_label = None

    for entity in ner_results:
        # Check if the current label matches the previous one
        if entity["entity"].startswith("B-") or (current_label and not entity["entity"].startswith("I-")):
            if current_entity:
                entities.append((current_entity, current_label))
            # Reset the current entity
            current_entity = entity["word"]
            current_label = entity["entity"]

        elif entity["entity"].startswith("I-") and not entity["word"].startswith("##"):
            current_entity += " " + entity["word"].replace("##", "")

        else:
            current_entity += entity["word"].replace("##", "")  # Merge tokens

    if current_entity:
        entities.append((current_entity, current_label))

    # Filter only organization entities
    company_names = [name for name, label in entities if label in ["B-ORG", "I-ORG"]]
    
    return company_names

def grabTicker(text):
    """
    Parses Tickers From Text (not perfect)

    Parameters:
    text (str)

    Returns: 
    tickers (set)
    """
    
    tickers = set()
    # tickerInfo = ticker_ner(text)

    # for entity in tickerInfo:
    #     print(entity)
    #     tickers.add(entity["word"].strip())

    ticker_pattern = r'\b[A-Z]{1,5}\b'
    potential_tickers = re.findall(ticker_pattern, text)
    
    tickers.update(potential_tickers)

    tickers.difference_update(common_financial_abbreviations)

    return tickers

def companyToTicker(companies):
    """
    Gets Ticker From Company Names 

    Parameters:
    companies (list)

    Returns: 
    tickers (set)
    """

    tickers = set()

    for company in companies:
        
        url = f"{base_url}/search?q={company}&exchange=US&token={finnhub_api_key}"
        lookup = requests.get(url)

        if lookup.status_code == 200:
            data = lookup.json()
        else:
            print(f"Error: {lookup.status_code}, {lookup.text}")

        if data["count"]:
            tickers.add(data["result"][0]["symbol"])

    return tickers
