from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import TextAreaField,TextField

class searchBar(FlaskForm):
    ta_name = StringField('ta_name', validators=[DataRequired()])