from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, TextField, TextAreaField
from wtforms.validators import InputRequired, Optional
import re


## settings forms ##
class SettingForm(FlaskForm):
    id = HiddenField()
    name = HiddenField('name')
    value = IntegerField('value',
                validators=[InputRequired()])
    notes = TextAreaField('notes', validators=[Optional()])


    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        failures = 0
        
        if re.search(r'hi-res data retention days', 
                     self.name.data, re.IGNORECASE):
            if int(self.value.data) < 7 or int(self.value.data) > 90: 
                self.value.errors.append('Value must be between 7 and 90')
                failures += 1
           
        if re.search(r'hourly-avg data retention days', 
                     self.name.data, re.IGNORECASE):
            if int(self.value.data) < 30 or int(self.value.data) > 365: 
                self.value.errors.append('Value must be between 30 and 365')
                failures += 1
           
        if re.search(r'store temperature fahrenheit', 
                     self.name.data, re.IGNORECASE):
            if int(self.value.data) not in (0,1): 
                self.value.errors.append('Value must be 1 (true) or 0 (false)')
                failures += 1
        
        if re.search(r'polling interval minutes', 
                     self.name.data, re.IGNORECASE):
            if int(self.value.data) < 1 or int(self.value.data) > 15: 
                self.value.errors.append('Value must be between 1 and 15')
                failures += 1

        if failures:
            return False

        return True

