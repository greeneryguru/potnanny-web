from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError, NumberRange, \
            InputRequired
from .models import Action
import re


class ActionForm(FlaskForm):
    id = HiddenField('id')
    action_target = HiddenField('action_target')
    type_id = SelectField('measurement type', validators=[InputRequired()])
    condition = SelectField('condition', choices=[('GT', 'greater than'), ('LT', 'less than'), ('EQ', 'equal to')], validators=[InputRequired()])
    value = IntegerField('trigger value', validators=[InputRequired()])
    action = SelectField('action', choices=[('switch-outlet', 'switch outlet'), ('sms-message', 'sms message')], validators=[InputRequired()])
    outlet = SelectField('outlet')
    action_state = BooleanField('state on/off')
    recipient = StringField('recipient mobile number')
    wait_time = IntegerField('wait minutes', default="5", validators=[InputRequired()])
    active = BooleanField('action is active', default="1")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if self.action.data == 'switch-outlet':
            if not self.outlet.data or self.outlet.data == "":
                self.outlet.errors.append("must select an outlet")
                return False

            self.action_target.data = self.outlet.data
 

        elif self.action.data == 'sms-message':
            if not self.recipient.data or self.recipient.data == "":
                self.recipient.errors.append("must provide a recipient mobile number")
                return False

            self.action_target.data = self.recipient.data 

        return True


