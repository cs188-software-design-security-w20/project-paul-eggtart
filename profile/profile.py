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

class User(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    authenticated = BooleanField('authenticated', default=False)
    password_reset = DateTimeField('password_reset')
    credits = IntegerField('credits', default=0)
    viewable_ta = FieldList('ta_name', StringField('name'))
    remaining_views = IntegerField('remaining_views', default=3)
