from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template
)
from custom_wtforms.forum_forms import comment_form, rating_form
from search import searchBar
from load import database

db = database()#define database



########################## Firebase Portion
import os
import pyrebase
from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES 
load_dotenv()
load_dotenv(verbose=True)
from pathlib import Path  
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
#LOAD ENVIRONMENT VARIABLES

config = {
    "apiKey": os.environ.get('FIREBASE_API_KEY'),
    "authDomain": "rate-my-ta.firebaseapp.com",
    "databaseURL": "https://rate-my-ta.firebaseio.com",
    "projectId": "rate-my-ta",
    "storageBucket": "rate-my-ta.appspot.com",
    "serviceAccount": "key/firebase-key.json",
    "messagingSenderId": "358133458427"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
########################## Firebase Portion


router = Blueprint(
    'router',
    __name__,
    template_folder='../templates'
)



@router.route('/TA/<ta_name>', methods=['GET', 'POST'])
def TA(ta_name):
    ta_info = []
    ta = db.child("TA").child(ta_name).get()
    name = ta.key()
    comments = []
    for _, val in ta.val().items():
        if val["comment"]:
            comments.append(val["comment"])
    ta_info.append((name,comments))

    # adding comment to forum
    my_comment = comment_form()
    if my_comment.validate_on_submit():
        print(my_comment.comment.data)
        db.child("TA").child(ta_name).push({"comment": my_comment.comment.data})
        return redirect('/TA/'+ta_name)
    
    # addint rating to TA
    my_rating = rating_form()
    if my_rating.validate_on_submit():
        print(my_rating.clarity.data)
        print(my_rating.helpfulness.data)
        print(my_rating.availability.data)
        db.child("Ratings").child(ta_name).push({"rating": [my_rating.clarity.data, my_rating.helpfulness.data, my_rating.availability.data]})

    return render_template('ta_page.html', ta_info=ta_info, redirect='/TA/'+ta_name, comment_form=my_comment, rating_form=my_rating, ta_jpg= ta_name+".jpg")



@router.route('/search', methods=['GET', 'POST'])
def search():
    search = searchBar()
    if search.validate_on_submit():
        return redirect('/TA/'+search.ta_name.data)
    return render_template('search.html', form=search)  



@router.route('/')
def home():
    return render_template('index.html')



@router.route('/login', methods=['GET'])
def login():
    username = "Nick"
    context = {
        "data": username
    }
    return render_template('login.html', **context)