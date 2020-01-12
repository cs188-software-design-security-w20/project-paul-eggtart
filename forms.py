from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import TextAreaField,TextField

from wtforms.fields.html5 import IntegerField

class forum(FlaskForm):
    comment = StringField('comment', validators=[DataRequired()])

class slider(FlaskForm):
    clarity = IntegerField('clarity', default=0)