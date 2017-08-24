from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from .models import Outlet

def unique_check(form, field):
    o = Outlet.query.filter_by(name=field.data).first()
    if o:
        raise ValidationError('Name must be unique')

class OutletForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators=[DataRequired(), unique_check])