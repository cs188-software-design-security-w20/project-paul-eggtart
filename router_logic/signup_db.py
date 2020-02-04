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

class signUp(FlaskForm):
    first_name = StringField('first_name', [validators.Length(min=1, max=50)])
    last_name = StringField('last_name', [validators.Length(min=1, max=50)])
    email_addr = StringField('email_addr', [validators.Length(min=1, max=50)])
    password = StringField('password', [validators.Length(min=1, max=50)])

def create_user(db, signup_form):
    print(signup_form.first_name.data)
    print(signup_form.last_name.data)
    new_user = User()
    new_user.id = 0
    new_user.email = signup_form.email_addr.data
    new_user.first_name = signup_form.first_name.data
    new_user.last_name = signup_form.last_name.data
    new_user.password = signup_form.password.data
    new_user.authenticated = True
    new_user.password_reset = None
    new_user.credits = 0
    new_user.viewable_ta = []
    new_user.remaining_views = 3
    db.child("users").push(jsonify(new_user))


# class User:
#     def __init__(self, first_name, last_name, email_addr, password):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email_addr = email_addr
#         self.password = password
#         self.authenticated = True
#         self.credits = 0
