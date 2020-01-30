from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template
)
from load import database
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField
from wtforms import DateTimeField
from wtforms import FieldList
from wtforms.validators import DataRequired
from wtforms import TextAreaField, TextField, validators
from wtforms.fields.html5 import IntegerField

db = database()

class User():
    id = IntegerField('id')
    email = StringField('email', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    authenticated = BooleanField('authenticated', default=False)
    password_reset = DateTimeField('password_reset')
    credits = IntegerField('credits', default=0)
    viewable_ta = FieldList('ta_name', StringField())
    remaining_views = IntegerField('remaining_views', default=3)

    def __init__(self):
        return
    
    def model_class(self):
        return User

    def get_user(self, db, username):
        user = db.child("users").child(username).get()
        for key, val in user.val().items():
            setattr(self, key, val)
        return self
    
    def update_user(self, form, **kwargs):
        cls = self.model_class()
        names = self.get_properties()
        attributes = self.validate_data(names, form)
        for key, val in list(attributes.items()):
            if val == '':
                del attributes[key]
        db.child("users").child(id).update(attributes)
        return "Success"

    def get_parameters(self):
        cls = self.model_class()
        parameters = []
        for name in cls.__dict__.keys():
            if hasattr(User, name) and not name.startswith('_') and not callable(getattr(User, name)):
                parameters.append({
                    "name": name
                })
        return parameters

    #returns array of properties
    def get_properties(self):
        cls = self.model_class()
        names = []
        for name in cls.__dict__.keys():
            if hasattr(User, name) and not name.startswith('_') and not callable(getattr(User, name)):
                names.append(name)
        return names

    def validate_data(self, names, params):
        attributes = {}
        for name in names:
            param = params.get(name)
            if param is not None:
                if hasattr(User, name):
                    attributes[name] = param
        return attributes






