import datetime
import json
import re
from potnanny.extensions import db
from potnanny.apps.sensor.models import Sensor


class MeasurementType(db.Model):
    __tablename__ = 'measurement_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, server_default='', 
                     unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def as_dict(self):
        return {'id': self.id, 'name': self.name, }


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
            'type': self.type_m,
            'value': self.value, 
            'date_time': datetime.datetime.strftime(self.date_time, 
                                                    "%m/%d/%y %H:%M"),
        }


class MeasurementAverage(db.Model):
    __tablename__ = 'measurement_averages'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('measurement_types.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))
    avg = db.Column(db.Float, nullable=False, server_default='0')
    min = db.Column(db.Float, nullable=False, server_default='0')
    max = db.Column(db.Float, nullable=False, server_default='0')
    date_time = db.Column(db.DateTime, nullable=False)

    measurement_type = db.relationship("MeasurementType",
                                       backref="measurement-avgs",
                                       single_parent=True,
                                       cascade="all, delete-orphan")
    sensor = db.relationship("Sensor",
                             backref="measurements-avgs",
                             single_parent=True,
                             cascade="all, delete-orphan")

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
                'date_time': datetime.datetime.strftime(self.date_time, 
                                                        "%m/%d/%y %H:%M"),
        }


