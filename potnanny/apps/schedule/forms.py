from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, SelectField
from wtforms.validators import ValidationError, InputRequired, DataRequired
from .models import Schedule
import re


def valid_time_check(form, field):
    if not re.search(r'^(\d\d?:\d\d?)\s*(am|pm)?$', field.data, re.IGNORECASE):
        raise ValidationError('Enter time like "7:35 PM" or "19:35"')


class ScheduleForm(FlaskForm):
    id = HiddenField('id')
    custom = HiddenField('custom', default="0")
    days = HiddenField('days', default="127")
    outlet_id = SelectField('Outlet', validators=[DataRequired()])
    on_time = StringField('ON time', 
                            validators=[
                                InputRequired(),
                                valid_time_check])
    off_time = StringField('OFF time', 
                            validators=[
                                InputRequired(),
                                valid_time_check])
    


