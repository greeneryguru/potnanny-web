from app import db
import datetime


class MeasurementType(db.Model):
    __tablename__ = 'measurement_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, server_default='', unique=True)
    code = db.Column(db.String(4), nullable=False, server_default='', unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))
    code = db.Column(db.String(4), index=True, nullable=False)
    value = db.Column(db.Integer, nullable=False, server_default='0')
    date_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, id, code, value, dt=datetime.datetime.now()):
        self.sensor_id = id
        self.code = code
        self.value = value
        self.date_time = dt

    def simplified(self):
        return {'id': self.id, 
                'sensor_id': self.sensor_id,
                'code': self.code, 
                'value': self.value, 
                'date_time': datetime.datetime.strftime(self.date_time, "%m/%d/%y %H:%M")}



