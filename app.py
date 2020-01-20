import os

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
import load

def create_app(config_file):
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    csrf = CSRFProtect()
    app.config['SECRET_KEY'] = os.environ.get("CSRF_KEY_SECRET")
    
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
    app.register_blueprint(css)
    return app

app = create_app('config')

limiter = Limiter(app,key_func=get_remote_address,default_limits=["20 per minute", "10 per second"])


@app.route('/')
def index():
    return redirect(url_for('router.home'))


if __name__ == '__main__':
    app.run()