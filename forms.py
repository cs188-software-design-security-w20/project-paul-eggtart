from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import TextAreaField,TextField

class forum(FlaskForm):
    comment = StringField('comment', validators=[DataRequired()])