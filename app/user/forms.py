from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, PasswordField, \
            BooleanField
from wtforms.validators import DataRequired, ValidationError, NumberRange, \
            InputRequired, Length
from .models import User


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


def passwords_match(form, field):
    if form.password1.data != form.password2.data:
        raise ValidationError('Passwords do not match')


class LoginForm(FlaskForm):
    username = StringField('username', 
                validators=[InputRequired()])
    password = PasswordField('password',
                validators=[InputRequired()])


class NewUserForm(FlaskForm):
    id = HiddenField()
    username = StringField('username', 
                validators=[InputRequired(),
                            unique_name_check])
    password1 = PasswordField('password',
                validators=[InputRequired(), Length(min=8, max=48), passwords_match])
    password2 = PasswordField('password again',
                validators=[InputRequired(), passwords_match])


class PasswordResetForm(FlaskForm):
    id = HiddenField()
    original = PasswordField('current password',
                validators=[InputRequired(), is_password])
    password1 = PasswordField('password',
                validators=[InputRequired(), Length(min=8, max=24), passwords_match])
    password2 = PasswordField('password again',
                validators=[InputRequired(), Length(min=8, max=24), passwords_match])




