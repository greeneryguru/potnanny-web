from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField
from wtforms.validators import DataRequired, ValidationError, NumberRange, \
            InputRequired
from .models import Setting
import re

def setting_check(form, field):
    if re.search('retention days', form.name.data, re.IGNORECASE):
        if int(field.data) < 7 or int(field.data) > 180: 
            raise ValidationError('Value must be between 7 and 180') 

    if re.search('polling interval minutes', form.name.data, re.IGNORECASE):
        if int(field.data) < 1 or int(field.data) > 15: 
            raise ValidationError('Value must be between 1 and 15') 

    if re.search('gpio.+pin', form.name.data, re.IGNORECASE):
        if int(field.data) < 0 or int(field.data) > 17: 
            raise ValidationError('Value must be between 0 and 17') 


class SettingForm(FlaskForm):
    id = HiddenField('id')
    name = HiddenField('name')
    value = IntegerField('value',
                validators=[InputRequired(),
                            setting_check])







