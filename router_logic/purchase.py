from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import TextAreaField, TextField, validators
from wtforms.fields.html5 import IntegerField
import requests

class purchase_form(FlaskForm):
    card = StringField('card', [validators.Length(min=1, max=50)])

    def process_payment(self,card_num): # returns true/false based on whether credit card was successfully processed
        PARAMS = {'card':card_num} 
          
        # sending get request and saving the response as response object 
        r = requests.get(url = "https://yanggatang.pythonanywhere.com/verify_card", params = PARAMS) 

        if r.text == "False":
            return False
        else: #not verified
            return True