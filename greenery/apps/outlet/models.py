from greenery import db
from greenery.lib.jsonmodel import JsonModel
from greenery.lib.rfutils import tx433
import json
import serial


class Outlet(db.Model, JsonModel):
    __tablename__ = 'outlets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, server_default='', unique=True)
    channel = db.Column(db.Integer, nullable=False, server_default='2', unique=True)
    state = db.Column(db.Boolean(), nullable=False, server_default='0')

    def __init__(self, name, channel):
        self.name = name
        self.channel = channel
        
    def __repr__(self):
        return json.dumps(self.as_dict())

    def on(self):
        rval = tx433(self.channel, 1)
        if not rval:
            self.state = 1
            db.session.commit()
        
        return str(self)

    def off(self):
        rval = tx433(self.channel, 0)
        if not rval:
            self.state = 0
            db.session.commit()

        return str(self)


