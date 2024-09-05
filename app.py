from flask import Flask, render_template, request, session
from apscheduler.schedulers.background import BackgroundScheduler
from info import grabSubInfo, searchSubInfo

#configure app
app = Flask(__name__)

subreddits = ["Stocks", "StockMarket", "Investing", "ValueInvesting", "Economics", "Technology", "Finance"]

# grab submission info
subInfo = grabSubInfo(subreddits)

def update_submissions():
    """Function to update submissions"""
    global subInfo
    subInfo = grabSubInfo(subreddits)

# Schedule updates every hour
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_submissions, trigger="interval", hours=1)
scheduler.start()

@app.route("/")
def index():
    """Show Top Submissions"""
    
    if subInfo == -1: return render_template("error.html"), 500 
    
    return render_template("home.html", submissions=subInfo)

@app.route("/search", methods=["POST"])
def search():
    """Search For Submissions"""

    if not request.form.get("query"):
        return render_template("home.html", submissions=subInfo)

    searchInfo = searchSubInfo(request.form.get("query"))
    if searchInfo == -1: return render_template("error.html"), 500
    return render_template("home.html", submissions=searchInfo)