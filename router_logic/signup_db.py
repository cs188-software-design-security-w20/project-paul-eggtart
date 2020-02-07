from flask import (
    current_app,
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
# ------ to send email conirmation
from email_db import send_email
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from extensions import mail
# ------
import json
import re


class SignUpForm(FlaskForm):
    first_name = StringField('first_name', [validators.Length(min=1, max=50)])
    last_name = StringField('last_name', [validators.Length(min=1, max=50)])
    email_addr = StringField('email_addr', [validators.Length(min=1, max=50)])
    password = StringField('password', [validators.Length(min=1, max=50)])

    def create_unauthenticated_user(self, db, signup_form):
        print(signup_form.first_name.data)
        print(signup_form.last_name.data)

        # SEND AN EMAIL CONFIRMATION
        self.send_confirmation_email(signup_form.email_addr.data)
        # CREATES A USER AND PUSHES IT INTO DB
        new_user = User()
        new_user.id = len(db.child("users").get().val())
        new_user.email = signup_form.email_addr.data
        new_user.first_name = signup_form.first_name.data
        new_user.last_name = signup_form.last_name.data
        new_user.password = new_user.encrypt(signup_form.password.data) # encrypt the password
        new_user.authenticated = False
        new_user.password_reset = None
        new_user.credits = 0
        new_user.viewable_ta = ""
        new_user.remaining_views = 3
        #print(json.loads(new_user.toJSON()))

        db.child("users").child(new_user.id).set(json.loads(new_user.toJSON()))
        db.child("users").child(new_user.id).child('viewable_ta').push({'name': "placeholder", 'rated': False})

    def verify_email(self, email):
        check_email = re.match(r'.*@(g\.)?ucla.edu$', email)
        if check_email != None:
            return True
        return False
    
    def check_existing_email(self, db, email):
        users = db.child("users").get()
        email = email.split('@')[0]
        for u in users.each():
            data = u.val()
            if data['email'].split('@')[0] == email:
                return False
        return True
    
    def send_confirmation_email(self, email_addr):
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

        confirm_url = url_for(
            'router.confirm_email',
            token=confirm_serializer.dumps(email_addr, salt='email-confirmation-salt'),
            _external=True
        )

        html = render_template(
            'email_confirmation.html',
            confirm_url=confirm_url
        )

        send_email('Confirm Your Email Address for Rate My TA', [email_addr], html)
