from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    jsonify,
    render_template
)
from flask_wtf import FlaskForm
from wtforms import Form
from wtforms.validators import DataRequired
from wtforms import TextAreaField, StringField, validators
from load import database
from profile.profile import User

db = database()

class LoginForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()]) 


    def login(self, user):
        decrypter = User() # we need the decrypt function from the user
        users = db.child("users").get()
        for u in users.each():
            data = u.val()
            if data['email'] == user.email and decrypter.decrypt(data["password"],user.password): #data["password"] == user.password:
                return int(data['id'])
        return -1
