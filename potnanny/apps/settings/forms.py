from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField
from wtforms.validators import InputRequired
import re


## settings forms ##
class SettingForm(FlaskForm):
    id = HiddenField()
    temperature = SelectField('temperature display',
                            choices=[('c', 'Celsius'),('f', 'Fahrenheit')],
                            validators=[InputRequired()])
    interval = SelectField('sensor polling',
                            choices=[('1', 'every minute'),
                                     ('2', 'every 2 minutes'),
                                     ('5', 'every 5 minutes'),
                                     ('10', 'every 10 minutes'),
                                     ('15', 'every 15 minutes')],
                            validators=[InputRequired()])
