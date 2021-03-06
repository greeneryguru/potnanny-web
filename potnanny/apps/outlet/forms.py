from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange, \
            InputRequired
from .models import Outlet


def unique_name_check(form, field):
    if form.id.data:
        o = Outlet.query.filter(
                Outlet.id != int(form.id.data), 
                Outlet.name == field.data).first()
    else:
        o = Outlet.query.filter_by(name=field.data).first()
    
    if o:
        raise ValidationError('Name must be unique')


def unique_channel_check(form, field):
    if form.id.data:
        o = Outlet.query.filter(
                Outlet.id != int(form.id.data), 
                Outlet.channel == int(field.data)).first()
    else:
        o = Outlet.query.filter_by(channel=int(field.data)).first()

    if o:
        raise ValidationError('Channel %s already in use.' % field.data)


class OutletForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', 
                validators=[
                    InputRequired(),
                    unique_name_check] )
                    
    on_code = IntegerField('on code',
                validators=[
                    InputRequired(),] )
    
    off_code = IntegerField('off code',
                validators=[
                    InputRequired(),] )
                    
   

