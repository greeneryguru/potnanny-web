import datetime
import json
from greenery import db
from greenery.apps.sensor.models import Sensor


class MeasurementType(db.Model):
    __tablename__ = 'measurement_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, server_default='', unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('measurement_types.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))
    value = db.Column(db.Float, nullable=False, server_default='0')
    text = db.Column(db.String(16), nullable=True)
    date_time = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, tid, sid, val, txt, 
                    dt=datetime.datetime.now().replace(
                        second=0, 
                        microsecond=0)):
        self.type_id = tid
        self.sensor_id = sid
        self.value = val
        self.text = txt
        self.date_time = dt

    def __repr__(self):
        return json.dumps(self.as_dict())

    def as_dict(self):
        return {'id': self.id,
                'type_id': self.type_id,
                'sensor_id': self.sensor_id,
                'value': self.value, 
                'text': self.text,
                'date_time': datetime.datetime.strftime(self.date_time, "%m/%d/%y %H:%M")}


class MeasurementAverage(db.Model):
    __tablename__ = 'measurement_averages'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('measurement_types.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))
    avg = db.Column(db.Float, nullable=False, server_default='0')
    min = db.Column(db.Float, nullable=False, server_default='0')
    max = db.Column(db.Float, nullable=False, server_default='0')
    date_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, tid, sid, navg, nmin, nmax, 
                    dt=datetime.datetime.now().replace(
                        minute=0, 
                        second=0, 
                        microsecond=0)):
        self.type_id = tid
        self.sensor_id = sid
        self.avg = navg
        self.min = nmin
        self.max = nmax
        self.date_time = dt


    def __repr__(self):
        return json.dumps(self.as_dict())


    def as_dict(self):
        return {'id': self.id, 
                'type_id': self.type_id,
                'sensor_id': self.sensor_id,
                'avg': self.avg, 
                'min': self.min,
                'max': self.max,
                'date_time': datetime.datetime.strftime(self.date_time, "%m/%d/%y %H:%M")}


