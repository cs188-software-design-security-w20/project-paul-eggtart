import os

from flask import (
    Flask,
    Blueprint,
    redirect,
    url_for
)
from router.router import router
from flask_wtf.csrf import CSRFProtect
import load

def create_app(config_file):
    app = Flask(__name__, static_url_path = "/images", static_folder = "images")
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





@app.route('/')
def index():
    return redirect(url_for('router.home'))


if __name__ == '__main__':
    app.run()