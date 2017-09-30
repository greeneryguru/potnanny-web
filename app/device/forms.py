import os
import sys
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, BooleanField, SelectField
from wtforms.validators import optional
from .models import Device, TxPwr433



class DeviceForm(FlaskForm):
    id = HiddenField('id')
    interface_id = HiddenField('interface_id')
    name = StringField('name')
    active = BooleanField('is active', default="1")
    interface_type = SelectField('interface type', choices=[
                                ('TxPwr433', '433Mhz Wireless power outlet'),
                                ('RxTemp433', '433Mhz Wireless temperature sensor'),
    ], default="TxPwr433")
    
    channel = IntegerField('channel', validators=[optional()])


    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if not self.unique_name_check():
            return False

        if self.interface_type.data == 'TxPwr433':
            if not self.unique_channel_check():
                return False

        
        return True


    def unique_name_check(self):
        if self.id.data:
            o = Device.query.filter(
                    Device.id != int(self.id.data), 
                    Device.name == self.name.data).first()
        else:
            o = Device.query.filter_by(name=self.name.data).first()
        
        if o:
            self.name.errors.append('Name must be unique')
            return False

        return True


    def unique_channel_check(self):
        """
        For Tx433 objects. ensure channel is unique
        """
        if not self.channel.data:
            self.channel.errors.append('Channel is required')
            return False

        if self.interface_id.data:
            o = TxPwr433.query.filter(
                    TxPwr433.id != int(self.interface_id.data), 
                    TxPwr433.channel == int(self.channel.data)).first()
        else:
            o = TxPwr433.query.filter_by(channel=int(self.channel.data)).first()

        if o:
            self.channel.errors.append('Channel %s already in use.' % self.channel.data)
            return False

        return True


