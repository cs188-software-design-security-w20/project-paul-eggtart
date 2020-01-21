from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import TextAreaField, StringField, validators
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def closest_match(search):
	choices = ["paul-eggert","tian-ye","jeff-bezos","tim-cook"]
	return process.extract(search, choices, limit=1)[0][0]

def closest_5_match(search):
	choices = ["paul-eggert","tian-ye","jeff-bezos","tim-cook"]
	return [name[0] for name in process.extract(search, choices, limit=5)]

class searchBar(FlaskForm):
    ta_name = StringField('ta_name', [validators.Length(min=1, max=50)])

