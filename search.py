from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import TextAreaField,StringField,validators

class searchBar(FlaskForm):
    #ta_name = StringField('ta_name', validators=[DataRequired()])
    ta_name = StringField('ta_name', [validators.Length(min=1, max=50)])