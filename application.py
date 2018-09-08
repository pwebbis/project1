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

#secret key
app.secret_key ='atum' ##TODO:mudar isto para mais seguro

##some property
#log_status = hidden
#ROUTES------------------------------------------------------------
@app.route("/")
def index():
    if 'username' in session:
        return render_template("logged_in.html")
    log_status = "hidden"
    return render_template("index.html",log_status=log_status)

#try to login and if so go on!!
@app.route("/logged_in", methods=['POST'])
def logged_in():
    if request.method=='POST': #TODO: talvez nao seja preciso o if como os cookies fazem o post automatico
        username_g = request.form.get("username")
        password_g = request.form.get("password")
        p_info=db.execute("SELECT (password) FROM users WHERE (username='%s')"%(username_g)).fetchall()
        log_status = "hidden"
        if not p_info:
            log_status = "visible"
            return render_template("index.html",log_status=log_status)
        else:
            p = p_info[0][0]


        if password_g == p:
            session['username']= username_g
            u_info = db.execute(f"SELECT (n_reviews, level) FROM users WHERE username='{username_g}'").fetchall()
            for u in u_info:
                print(u[0])
            return render_template("logged_in.html")
        else:
            log_status = "visible"
            return render_template("index.html",log_status=log_status)



@app.route("/log_out")
def log_out():
    session.pop('username',None)
    return render_template("index.html",log_status="hidden")



#create account page!!
@app.route("/create_acc",methods=['POST','GET'])
def create_acc():
    #default variables
    create_acc_status = "hidden"
    user_used="hidden"

    #get input variables
    create_user = request.form.get("username_reg")
    create_password = request.form.get("password_reg")
    create_name = request.form.get("first_name_reg")
    create_age = request.form.get("age_reg")
    create_gender= request.form.get("gender_reg")

    #process data/requests
    if request.method== 'POST':
        usr_list = db.execute("SELECT username FROM users").fetchall()
        users = [r[0] for r in usr_list]
        for user in users:
            print (user)
            if (user) == create_user:
                print("true")
                return render_template("create_acc.html", user_used="visible", create_acc_status="hidden")

        if (create_user and create_password and create_name and create_age and create_gender):

            db.execute("INSERT INTO users (username,password,first_name,age,gender) VALUES(:username, :password, :first_name, :age, :gender)",{"username":create_user, "password":create_password, "first_name":create_name,"age":create_age,"gender":create_gender})
            i = db.commit()

            log_status = "hidden"
            return render_template("index.html",log_status=log_status, user_used="hidden" )
        else:
            create_acc_status = "visible"
            return render_template("create_acc.html",create_acc_status=create_acc_status, user_used="hidden")
    else:
        return render_template("create_acc.html", create_acc_status="hidden", user_used="hidden")

@app.route("/test_style")
def test_style():
    return render_template("test_style.html")



#######################TODO: -layouts!!!
