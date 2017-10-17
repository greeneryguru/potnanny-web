from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, PasswordField, \
    BooleanField
from wtforms.validators import DataRequired, ValidationError, NumberRange, \
    InputRequired, Length, EqualTo, Email
from .models import User
import re

## custom validators ##
def setting_check(form, field):
    if re.search('retention days', form.name.data, re.IGNORECASE):
        if int(field.data) < 7 or int(field.data) > 90: 
            raise ValidationError('Value must be between 7 and 90') 

    if re.search('polling interval minutes', form.name.data, re.IGNORECASE):
        if int(field.data) < 1 or int(field.data) > 15: 
            raise ValidationError('Value must be between 1 and 15') 

    if re.search('gpio.+pin', form.name.data, re.IGNORECASE):
        if int(field.data) < 0 or int(field.data) > 17: 
            raise ValidationError('Value must be between 0 and 17') 


def unique_name_check(form, field):
    if form.id.data:
        o = User.query.filter(
                User.id != int(form.id.data), 
                User.username == field.data).first()
    else:
        o = User.query.filter_by(username=field.data).first()
    
    if o:
        raise ValidationError('Username already exists')


def is_password(form, field):
    u = User.query.get(int(form.id.data))
    if not u:
        raise ValidationError('Account error')

    if not u.check_password(field.data):
        raise ValidationError('Login Error')


## user forms ##
class LoginForm(FlaskForm):
    username = StringField('username', 
                validators=[InputRequired()])
    password = PasswordField('password',
                validators=[InputRequired()])


class UserEditForm(FlaskForm):
    id = HiddenField()
    username = StringField('username', 
                validators=[InputRequired(),
                            unique_name_check])
    email = StringField('email', validators=[Email()])


class PasswordResetForm(FlaskForm):
    id = HiddenField()
    original = PasswordField('current password',
                validators=[InputRequired(), is_password])
    password = PasswordField('password',
                validators=[InputRequired(), Length(min=8, max=24), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('password again', validators=[InputRequired()])


## settings forms ##
class SettingForm(FlaskForm):
    id = HiddenField()
    name = HiddenField('name')
    value = IntegerField('value',
                validators=[InputRequired(),
                            setting_check])

class TwilioForm(FlaskForm):
    id = HiddenField()
    sid = StringField('account SID', validators=[InputRequired()])
    token = StringField('account token', validators=[InputRequired()])
    number = StringField('phone number', validators=[InputRequired()])



