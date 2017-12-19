from greenery import db
from greenery.apps.measurement.models import MeasurementType
from greenery.apps.outlet.models import Outlet
import datetime


class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    measurement_id = db.Column(db.Integer, db.ForeignKey('measurement_types.id'))
    outlet_id = db.Column(db.Integer, db.ForeignKey('outlets.id'))
    action_type = db.Column(db.String(24), nullable=False, server_default='sms-message')
    sms_recipient = db.Column(db.String(24), nullable=True)
    
    """
    Here, the 'on' columns are also used to store one time sms-message 
    conditions as well, if the action-type is sms-message and not switch-outlet.
    """
    on_condition = db.Column(db.String(16), nullable=True)
    on_threshold = db.Column(db.Integer, nullable=True)

    off_condition = db.Column(db.String(16), nullable=True)
    off_threshold = db.Column(db.Integer, nullable=True)

    wait_minutes = db.Column(db.Integer, nullable=False, server_default='10')
    enabled = db.Column(db.Boolean(), nullable=False, server_default='1')

    outlet = db.relationship("Outlet")
    measurement = db.relationship("MeasurementType")
    

    def __init__(self, name, mid, oid, atype):
        self.name = name
        self.measurement_id = mid
        self.outlet_id = oid
        self.action_type = atype

    def __repr__(self):
        if not self.enabled:
            return (self.name + " *")
        else:
            return self.name

        """
        if self.action_type == 'sms-message':
            # returns like;
            # "temperature lt 65 sms-message +14015551212"
            msg = "%s %s %d %s %s" % (self.measurement, self.sms_condition,
                                self.sms_threshold, self.action_type,
                                self.sms_recipient)

        elif self.action_type == 'switch-outlet':
            # returns like;
            # "switch-outlet fans when temperature (gt 80 On/lt 75 Off)"
            # "switch-outlet irrigation when soil-moisture (lt 25 On/gt 35 Off)"
            msg = "%s %s when %s (%s %d ON, %s %d OFF)" % (self.action_type,
                                self.outlet, self.measurement, 
                                self.on_condition, self.on_threshold, 
                                self.off_condition, self.off_threshold)

        return msg
        """


"""
Track the state of Actions that have been triggered, and may or may not
yet be completed.
"""
class ActionProcess(db.Model):
    __tablename__ = 'action_processes'
    id = db.Column(db.Integer, primary_key=True)
    action_id = db.Column(db.Integer, db.ForeignKey('actions.id'))
    
    """
    Here, the 'on' columns are also used to store sms-message triggers as well,
    if the action-type is sms-message and not switch-outlet.
    """
    on_datetime = db.Column(db.DateTime, nullable=True)
    on_trigger = db.Column(db.String(24), nullable=True)

    off_datetime = db.Column(db.DateTime, nullable=True)
    off_trigger = db.Column(db.String(24), nullable=True)

    active = db.Column(db.Boolean(), nullable=False, server_default='1')
    action = db.relationship("Action")

    def __init__(self, aid):
        self.action_id = aid
        
    def assign_datetime(self, field, dt):
        setattr(self, field, dt.replace(second=0, microsecond=0))


