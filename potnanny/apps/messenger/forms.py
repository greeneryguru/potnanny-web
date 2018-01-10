from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import ValidationError, InputRequired
from .models import TwilioAccount, Messenger

class TwilioForm(FlaskForm):
    id = HiddenField()
    sid = StringField('account SID', validators=[InputRequired()])
    token = StringField('account token', validators=[InputRequired()])
    number = StringField('account phone number', validators=[InputRequired()])
    
    """
    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        test = Messenger()
        rval = test.test_message()
        print(rval)
        
        if rval:
            self.number.errors.append("account settings denied by twilio. please check settings")
            return False
        
        return True
    """
    
class TestMessageForm(FlaskForm):
    recipient = StringField('recipient number', validators=[InputRequired()])
    message = StringField('message', validators=[InputRequired()])
    
    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        m = Messenger()
        rval = m.message(self.recipient.data, self.message.data)
        # should return an id
        if rval:
            self.message.errors.append("Message failed. Please confirm Twilio Account settings")
            return False
        
        return True
    
    