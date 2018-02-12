from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, SelectField, \
    BooleanField
from wtforms.validators import DataRequired, ValidationError, NumberRange, \
    InputRequired, Optional
from .models import Action
import re


class ActionForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('action name', validators=[InputRequired()])
    measurement_type = SelectField('action triggered by measurement', validators=[InputRequired()])
    sensor_address = SelectField('triggered by sensor', choices=[('any', 'Any')], validators=[InputRequired()])
    outlet_id = SelectField('power outlet', validators=[Optional()])
    action_type = SelectField('action type', validators=[InputRequired()])
    sms_recipient = StringField('message recipient mobile number', validators=[Optional()])
    on_condition = SelectField('ON condition', choices=[('GT', 'greater than'), ('LT', 'less than'), ('EQ', 'equal to')])
    on_threshold = IntegerField('ON value')
    off_condition = SelectField('OFF condition', choices=[('GT', 'greater than'), ('LT', 'less than'), ('EQ', 'equal to')])
    off_threshold = IntegerField('OFF value', validators=[Optional()])
    wait_minutes = IntegerField('wait minutes after completion', default="5", validators=[InputRequired()])
    active = BooleanField('action is enabled', default="1")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if re.search(r'switch', self.action_type.data, re.IGNORECASE):
            failures = 0
            if not self.outlet_id.data or self.outlet_id.data == "":
                self.outlet_id.errors.append("must select an outlet")
                failures += 1

            if not self.on_condition.data:
                self.on_condition.errors.append("ON condition required")
                failures += 1

            if not self.on_threshold.data or self.on_threshold.data == "":
                self.on_value.errors.append("ON threshold value required")
                failures += 1

            if not self.off_condition.data:
                self.off_condition.errors.append("OFF condition required")
                failures += 1

            if not self.off_threshold.data or self.off_threshold.data == "":
                self.off_value.errors.append("OFF threshold value required")
                failures += 1

            if self.on_condition.data == self.off_condition.data:
                self.off_condition.errors.append("On and Off conditions should not be set to the same value. This will prevent an Action from working correctly.")
                failures += 1
                
            if failures:
                return False

        if re.search(r'sms', self.action_type.data, re.IGNORECASE):
            if not self.sms_recipient.data or self.sms_recipient.data == "":
                self.recipient.errors.append("recipient mobile number required")
                return False

        return True


