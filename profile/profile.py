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
from wtforms import Form
from wtforms import StringField
from wtforms import BooleanField
from wtforms import DateTimeField
from wtforms import FieldList
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms import TextAreaField, TextField, validators
from wtforms.fields.html5 import IntegerField
from flask_login import UserMixin
from flask_login import current_user
# ----- password db encryption portion
import bcrypt



import json

db = database()

class User(UserMixin):
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


    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

    def __init__(self):
        return
    
    def get_id(self):
        try:
            user_list = db.child("users").get()
            for i in user_list.each():
                if(i.val() is not None):
                    if self.email == (i.val()["email"]): #return the id associated with this email
                        return i.val()["id"]
        except AttributeError:
            raise NotImplementedError("No id found")

    def get(self, id):
        try:
            return User
        except:
            return None

    def model_class(self):
        return User


    def get_user(self, db, username):
        user = db.child("users").child(username).get()
        data = user.val()
        for key, val in user.val().items():
            setattr(self, key, val)

        ta_list = []
        for ta in self.viewable_ta:
            ta_list.append(str(data["viewable_ta"][ta]['name']))

        return self, ta_list
    
    def update_user(self, form, **kwargs):
        cls = self.model_class()
        names = self.get_properties()
        attributes = self.validate_data(names, form)
        for key, val in list(attributes.items()):
            if val == '':
                del attributes[key]
        id = attributes["id"]
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

    def number_views(self):
        id_user = current_user.id
        current_session_user = db.child("users").child(id_user).get().val()

        if (current_session_user is not None):
            num_views = current_session_user['remaining_views']
            return num_views
        else:
            return None

    def decrement_views(self, name_of_ta):
        # Otherwise, decrement views by 1, update DB
        id_user = current_user.id
        current_session_user = db.child("users").child(id_user).get().val()
        ta_viewable_list = db.child("users").child(id_user).child('viewable_ta').get()
        for _, val in ta_viewable_list.val().items():
            if val['name'] == name_of_ta:
            # If the TA is one of their viewable TAs, don't decrement views
                return
        current_session_user['remaining_views'] = current_session_user['remaining_views'] - 1
        db.child("users").child(id_user).update(current_session_user) # update db with new number of views
                
        ta_viewable_list2 = db.child("users").child(current_user.id).child('viewable_ta')
        ta_viewable_list2.push({'name': name_of_ta, 'rated': False}) # update ta's that this person has seen
        return 


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def encrypt(self,password_plain):
        passwd = password_plain.encode('utf-8')

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwd, salt)

        return hashed.decode('utf-8') # convert it to string

    def decrypt(self,password_hashed,password_plain):
        if bcrypt.checkpw(password_plain.encode('utf-8'),password_hashed.encode('utf-8')):
            #match
            return True
        else:
            return False
