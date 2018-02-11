from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, BooleanField
from wtforms.validators import DataRequired, ValidationError, NumberRange, \
            InputRequired
from .models import Sensor


class SensorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators=[InputRequired()])
    address = StringField('address', render_kw={'readonly': True})





