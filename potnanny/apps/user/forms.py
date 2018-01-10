from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, BooleanField
from wtforms.validators import ValidationError, InputRequired, Email, \
    Optional, Length, EqualTo
from .models import User
import re

def is_password(form, field):
    u = User.query.get(int(form.id.data))
    if not u:
        raise ValidationError('Account error')

    if not u.check_password(field.data):
        raise ValidationError('Login Error')
    
    
def unique_name_check(form, field):
    if form.id.data:
        u = User.query.filter(
                User.id != int(form.id.data),
                User.username == field.data).first()
    else:
        u = User.query.filter(User.username == field.data).first()

    if u:
        raise ValidationError('Name must be unique')


class UserForm(FlaskForm):
    id = HiddenField('id')
    username = StringField('name',
                validators=[InputRequired(),
                            unique_name_check])
    email = StringField('email', validators=[Optional()])
    active = BooleanField('account enabled', default="1")


class LoginForm(FlaskForm):
    username = StringField('username', 
                validators=[InputRequired()])
    password = PasswordField('password',
                validators=[InputRequired()])


class PasswordResetForm(FlaskForm):
    id = HiddenField()
    original = PasswordField('current password',
                validators=[InputRequired(), is_password])
    password = PasswordField('new password',
                validators=[InputRequired(), Length(min=8, max=24), 
                            EqualTo('confirm', 
                                    message='Passwords must match')])
    confirm = PasswordField('password again', validators=[InputRequired()])



