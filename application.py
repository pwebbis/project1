import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

#move this to ...
res = requests.get("https://www.goodreads.com/book/review_counts.json",
params={"key": "ai13CjUEI3y4JJeZdmIkg", "isbns": "9781632168146"})
#print(res.json())
##-------------------------

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

##some property
#log_status = hidden
#ROUTES------------------------------------------------------------
@app.route("/")
def index():
    log_status = "hidden"
    return render_template("index.html",log_status=log_status)

@app.route("/logged_in", methods=['POST'])
def logged_in():
    username_g = request.form.get("username")
    password_g = request.form.get("password")
    p_info=db.execute("SELECT (password) FROM users WHERE (username='%s')"%(username_g)).fetchall()

    if not p_info:
        log_status = "visible"
        return render_template("index.html",log_status=log_status)
    else:
        p = p_info[0][0]


    if password_g == p:
        return render_template("logged_in.html")
    else:
        log_status = "visible"
        return render_template("index.html",log_status=log_status)



@app.route("/create_acc")
def create_acc():
    return render_template("create_acc.html")
