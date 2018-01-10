from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, BooleanField
from wtforms.validators import DataRequired, ValidationError, NumberRange, \
            InputRequired
from .models import Sensor


def unique_name_check(form, field):
    if form.id.data:
        o = Sensor.query.filter(
                Sensor.id != int(form.id.data), 
                Sensor.name == field.data).first()
    else:
        o = Sensor.query.filter_by(name=field.data).first()
    
    if o:
        raise ValidationError('Name already used')


class SensorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators=[InputRequired(), unique_name_check])
    tags = StringField('tags', validators=[InputRequired()])
    address = IntegerField('address', validators=[InputRequired()])
    active = BooleanField('sensor enabled', default="1")





