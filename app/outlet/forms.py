from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField
from wtforms.validators import DataRequired, ValidationError
from .models import Outlet

def unique_check(form, field):
    o = Outlet.query.filter_by(name=field.data).first()
    if o:
        raise ValidationError('Name must be unique')

def unique_channel_check(form, field):
    o = Outlet.query.filter_by(channel=int(field.data)).first()
    if o:
        raise ValidationError('Channel %s already in use.' % field.data)
        
class OutletForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', 
                validators=[DataRequired(), unique_check])
    channel = SelectField('channel', 
                choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5')],
                validators=[unique_channel_check])