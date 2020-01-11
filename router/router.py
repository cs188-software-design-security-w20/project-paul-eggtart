from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template

)

from forms import forum
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

@router.route('/TA-Paul-Eggtart', methods=['GET', 'POST'])
def TA_Paul_Eggtart():
    return render_template('ta_page.html')


@router.route('/debug', methods=['GET', 'POST'])
def debug():
    ta_arr_db = db.child("TA").get()
    ta_arr = []
    for ta in ta_arr_db.each():
      name = ta.key() #name
      comments = []
      for _, val in ta.val().items():
        comments.append(val['comment'])
      ta_arr.append( (name,comments))

    return render_template('debug.html',ta_arr=ta_arr)



@router.route('/submit', methods=['GET', 'POST'])
def submit():
    form = forum()
    if form.validate_on_submit():
        db.child("TA").child("Paul Eggert").push({"comment": form.comment.data})
        return redirect('/TA-Paul-Eggtart')
    return render_template('register.html', form=form)



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


