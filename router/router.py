from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template
)

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

@router.route('/TA-Paul-Eggtart', methods=['GET'])
def TA_Paul_Eggtart():
    data = {"name": "Joe Tilsed"}
    db.child("users").child("Joe").set(data)
    return render_template('ta_page.html')

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


