from flask import Flask, render_template, request, session

from info import grabSubInfo, searchSubInfo

#configure app
app = Flask(__name__)

subreddits = ["Stocks", "StockMarket", "Investing", "ValueInvesting", "Economics", "Technology", "Finance"]

# grab submission info
subInfo = grabSubInfo(subreddits)

@app.route("/")
def index():
    """Show Top Submissions"""
    
    return render_template("home.html", submissions=subInfo)

@app.route("/search", methods=["POST"])
def search():
    if not request.form.get("query"):
        subInfo = grabSubInfo(subreddits)
        return render_template("home.html", submissions=subInfo)

    searchInfo = searchSubInfo(request.form.get("query"))
    return render_template("home.html", submissions=searchInfo)