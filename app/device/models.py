import os
import sys
from app import db
from sqlalchemy_utils import generic_relationship


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48), index=True, nullable=False, server_default='', unique=True)
    device_type = db.Column(db.Integer, nullable=False, server_default="1")
    active = db.Column(db.Boolean(), nullable=False, server_default='1')
    interface_type = db.Column(db.String(48), nullable=False)
    interface_id = db.Column(db.Integer, nullable=False)
    interface = generic_relationship(interface_type, interface_id)  

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


"""
Interface Class for devices that will accept simple On-Off Keyed (OOK) 
transmitted codes over 433Mhz to turn on/off.
Examples are:
    - wireless power outlet
    - wireless bulb sockets
    - garage doors?

    API for the interface is:
        on()
        off()
"""
class TxPwr433(db.Model):
    __tablename__ = 'tx433'
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.Integer, nullable=False, server_default='2', unique=True)
    state = db.Column(db.Boolean, nullable=False, server_default="0")

    def __init__(self, channel, state=0):
        self.channel = channel
        self.state = state

    def __repr__(self):
        return "chan=%d state=%d" % (self.channel, self.state) 

    def on(self):
        if self.state == 0:
            self.state = 1
            print("on!")

    def off(self):
        if self.state == 1:
            self.state = 0
            print("off!")




