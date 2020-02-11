from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    jsonify,
    flash,
    render_template
)
from flask_wtf import FlaskForm
from wtforms import Form
from wtforms.validators import DataRequired
from wtforms import TextAreaField, StringField, validators
from load import database
from profile.profile import User
import datetime

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
                if data['authenticated'] is False:
                    flash("Account not authenticated. Please reauthenticate.")
                    return -2
                reset_date = data['password_reset']
                reset_date_obj = datetime.datetime.strptime(reset_date, '%Y-%m-%dT%H:%M:%S.%f')
                if reset_date_obj < datetime.datetime.now():
                    flash("Password has expired. Please reset your password")
                    return -3
                return int(data['id'])
        return -1
