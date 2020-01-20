from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import TextAreaField, StringField, validators
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def closest_match(search):
	choices = ["paul-eggert","tian-ye"]
	return process.extract(search, choices, limit=1)[0][0]

class searchBar(FlaskForm):
    ta_name = StringField('ta_name', [validators.Length(min=1, max=50)])

