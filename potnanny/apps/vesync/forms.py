from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import InputRequired, Optional
from .models import VesyncApi
import hashlib

## settings forms ##
class VesyncForm(FlaskForm):
    id = HiddenField('id')
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])

    def validate(self):
        try:
            hashed = hashlib.md5(self.password.data.encode('utf-8')).hexdigest()
            api = VesyncApi(self.username.data, hashed)
        except:
            self.username.errors = ('Connection declined. Please verify VeSync username and password information.',)
            return False
        
        return True

