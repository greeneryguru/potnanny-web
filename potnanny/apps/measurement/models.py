import datetime
import json
import re
from potnanny.extensions import db
from potnanny.apps.sensor.models import Sensor


class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.String(24), nullable=False, index=True)
    type_m = db.Column(db.String(24), nullable=False, index=True)
    value = db.Column(db.Float, nullable=False, server_default='0')
    date_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, 
                 address, 
                 type_m, 
                 val, 
                 dt=datetime.datetime.now().replace(second=0,microsecond=0)):
        
        self.sensor = address
        self.type_m = type_m
        self.value = val
        self.date_time = dt

    def __repr__(self):
        return json.dumps(self.as_dict())

    def as_dict(self):
        return {
            'id': self.id,
            'sensor': self.sensor,
            'type_m': self.type_m,
            'value': self.value, 
            'date_time': datetime.datetime.strftime(self.date_time, 
                                                    "%m/%d/%y %H:%M"),
        }



