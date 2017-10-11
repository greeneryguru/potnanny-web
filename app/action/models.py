from app import db
from app.measurement.models import MeasurementType
import datetime

class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('measurement_types.id'))
    condition = db.Column(db.String(8), nullable=False, server_default='gt')
    value = db.Column(db.Integer, nullable=False, server_default='0')    
    active = db.Column(db.Boolean(), nullable=False, server_default='1')
    wait_time = db.Column(db.Integer, nullable=False, server_default='0')
    action = db.Column(db.String(24), nullable=True, server_default='')
    action_target = db.Column(db.String(24), nullable=True, server_default='')
    action_state = db.Column(db.Boolean(), nullable=True, server_default='1')

    measurement = db.relationship("MeasurementType")

    def __repr__(self):
        msg = "%s %s %d %s " % (str(self.measurement), self.condition, self.value, self.action.split("-")[0])
        if self.action == 'switch-outlet':
            state = 'on' if self.action_state else 'off'
            msg += "%s %s"  % (self.action_target, state)
        elif self.action == 'sms-message':
            msg += "%s" % self.action_target

        if not self.active:
            msg += " *"

        return msg


class ActionProcess(db.Model):
    __tablename__ = 'action_processes'
    id = db.Column(db.Integer, primary_key=True)
    action_id = db.Column(db.Integer, db.ForeignKey('actions.id'))
    date_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, id, dt=datetime.datetime.now()):
        self.action_id = id
        self.date_time = dt


