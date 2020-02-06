import os
from flask_login import LoginManager, login_manager
from flask import (
    Flask,
    Blueprint,
    redirect,
    url_for
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address # limiter against DDOS
from router.router import router
from flask_wtf.csrf import CSRFProtect
from profile.profile import User
import load


login_manager = LoginManager()

def create_app(config_file):
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    csrf = CSRFProtect()
    app.config['SECRET_KEY'] = os.environ.get("CSRF_KEY_SECRET")
    app.secret_key = b'\x06\x82\x96n\xfa\xbb(L\x97n\xb8.c\\y\x8a'
    login_manager.init_app(app)
    csrf.init_app(app)
    app.config.from_object(config_file)
    app.register_blueprint(router, url='/router')
    css = Blueprint(
        'css',
        __name__,
        template_folder='templates',
        static_folder='static/css',
        static_url_path='/static/css'
    )
    js = Blueprint(
        'js',
        __name__,
        template_folder='templates',
        static_folder='static/js',
        static_url_path='/static/js'
    )
    app.register_blueprint(js)

    return app

app = create_app('config')

db = load.database()
limiter = Limiter(app,key_func=get_remote_address,default_limits=["20 per minute", "10 per second"])


@login_manager.user_loader
def load_user(user_id):

    print("USER IS HERE GOGOGOGOGOGOGO")
    user_data = db.child("users").child(user_id).get()
    user = User(0)
    if(user_data.val() is not None):
        user.id = user_data.val()["id"]
        user.email = user_data.val()["email"]
    return user

@app.route('/')
def index():
    return redirect(url_for('router.home'))



if __name__ == '__main__':
    app.run()