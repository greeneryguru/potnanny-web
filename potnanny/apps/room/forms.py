from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, BooleanField
from wtforms.validators import DataRequired, ValidationError, NumberRange, \
            InputRequired
from .models import Room


class RoomForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators=[InputRequired()])




