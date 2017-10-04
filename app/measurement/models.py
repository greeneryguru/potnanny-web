from app import db
import datetime


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
    value = db.Column(db.Integer, nullable=False, server_default='0')
    date_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, type_id, value, dt=datetime.datetime.now()):
        self.type_id = type_id
        self.value = value
        self.date_time = dt

    def simplified(self):
        return {'id': self.id, 
                'type_id': self.type_id, 
                'value': self.value, 
                'date_time': datetime.datetime.strftime(self.date_time, "%m/%d/%y %H:%M")}


    def __repr__(self):
        return ",".join((str(self.id), str(self.type_id), str(self.value), str(self.date_time)))


