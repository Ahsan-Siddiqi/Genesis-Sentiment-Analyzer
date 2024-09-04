from flask import Flask, render_template, request, session

from info import grabSubInfo

#configure app
app = Flask(__name__)

subreddits = ["Stocks", "StockMarket", "Investing", "ValueInvesting", "Economics", "Technology", "Finance"]

# grab submission info
subInfo = grabSubInfo(subreddits)

@app.route("/")
def index():
    """Show Top Submissions"""
    
    return render_template("home.html", submissions=subInfo)