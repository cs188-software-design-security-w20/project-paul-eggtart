from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    jsonify,
    render_template
)
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import TextAreaField, StringField, validators
from load import database
from profile.profile import User
import json

class SignUpForm(FlaskForm):
    first_name = StringField('first_name', [validators.Length(min=1, max=50)])
    last_name = StringField('last_name', [validators.Length(min=1, max=50)])
    email_addr = StringField('email_addr', [validators.Length(min=1, max=50)])
    password = StringField('password', [validators.Length(min=1, max=50)])

    def create_user(self, db, signup_form):
        print(signup_form.first_name.data)
        print(signup_form.last_name.data)
        new_user = User(len(db.child("users").get().val()))
        new_user.email = signup_form.email_addr.data
        new_user.first_name = signup_form.first_name.data
        new_user.last_name = signup_form.last_name.data
        new_user.password = signup_form.password.data
        new_user.authenticated = True
        new_user.password_reset = None
        new_user.credits = 0
        new_user.viewable_ta = []
        new_user.remaining_views = 3
        db.child("users").child(new_user.id).set(json.loads(new_user.toJSON()))

    # def verify_email(self, email):
