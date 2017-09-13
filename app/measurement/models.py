from app import db
import datetime
from app.sensor.models import Sensor

class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    data_type = db.Column(db.String(16), nullable=False, server_default='')
    value = db.Column(db.Integer, nullable=False, server_default='0')
    date_time = db.Column(db.DateTime, nullable=False, server_default=datetime.datetime.utcnow)

    sensor = db.relationship('Sensor',
                           backref=db.backref('sensors', cascade="all, delete-orphan"), lazy='joined')


    def __init__(self, sensor_id, data_type, value, dtime):
        self.sensor_id = sensor_id
        self.data_type = data_type
        self.value = value
        self.date_time = dtime


    def __repr__(self):
        return ",".join(str(id), str(sensor_id), data_type, str(value), datetime)


