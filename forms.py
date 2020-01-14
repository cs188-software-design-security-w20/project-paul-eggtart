from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import TextAreaField,TextField,validators

from wtforms.fields.html5 import IntegerField


class forum(FlaskForm):
    comment = StringField('comment', [validators.Length(min=1, max=300)])

class slider(FlaskForm):
    clarity = IntegerField('clarity', default=0)