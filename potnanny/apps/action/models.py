from potnanny.extensions import db
from potnanny.apps.measurement.models import MeasurementType, Measurement
from potnanny.apps.outlet.models import Outlet
from potnanny.apps.messenger.models import Messenger
import datetime
import re


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
    active = db.Column(db.Boolean(), nullable=False, server_default='1')

    outlet = db.relationship("Outlet",
                             backref=db.backref("actions", 
                                                cascade="all,delete"))
    measurement = db.relationship("MeasurementType",
                                  backref=db.backref("actions", 
                                                cascade="all,delete"))
    

    def __init__(self, name, mid, oid, atype):
        self.name = name
        self.measurement_id = mid
        self.outlet_id = oid
        self.action_type = atype

    def __repr__(self):
        if not self.active:
            return (self.name + " *")
        else:
            return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'measurement': self.measurement,
            'outlet': self.outlet,
            'on_condition': self.on_condition,
            'on_threshold': self.on_threshold,
            'off_condition': self.off_condition,
            'off_threshold': self.off_threshold,
            'wait_minutes': self.wait_minutes,
            'active': self.active,
        }   


"""
The ActionProcess model keeps track of Actions that have been triggered, and 
may or may not yet be completed.
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
    action = db.relationship("Action",
                             backref=db.backref("processes", 
                                                cascade="all,delete"))

    def __init__(self, aid):
        self.action_id = aid
        
    def assign_datetime(self, field, dt):
        setattr(self, field, dt.replace(second=0, microsecond=0))

    def as_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'on_datetime': self.on_datetime,
            'on_trigger': self.on_trigger,
            'off_datetime': self.off_datetime,
            'off_trigger': self.off_trigger,
            'active': self.active,
        }
        
 
"""
ActionManager manages all interactions between Actions, Measurements, and 
the related ActionProcesses. 
Also, Switching outlets on/off, or sending sms messages when required.
"""
class ActionManager(object):
    
    def init_action(self, action, then=None, now=None):                    
        """
        evaluate measurements for an action within a timeframe,
        and process anything that requires an action
        
        params:
            1. Action obj. eval Measurements related to this object.
            2. Datetime obj. beginning of the time range to eval
            3. Datetime obj. end of the time range to eval 
        returns:
            None
        """
        if not now:
            now = datetime.datetime.now().replace(second=0, microsecond=0)
            
        if not then:
            then = now - datetime.timedelta(minutes=1)
            
        measurements = Measurement.query.filter(
            Measurement.type_id == action.measurement_id,
            Measurement.date_time.between(then,now)
        ).all()
    
        if not measurements:
            return

        for m in measurements:
            self.handle_action_measurement(action, m)


    def get_process(self, action, trigger=None):
        """
        get the active ActionProcess for an Action, if one exists.
        if not, create a new one.
        
        params:
            Action obj
            An optional trigger string ('on' or 'off'). This is used
            to determine if we should create a new process or not.
        returns:
            ActionProcess obj (None on error)
        """
        process = ActionProcess.query.filter(
            ActionProcess.active == True,
            ActionProcess.action_id == action.id
        ).first()
    
        if not process:
            if trigger and trigger == 'off':
                # we don't create new processes for an initial 'off' trigger
                return None
            
            process = ActionProcess(action.id)
            db.session.add(process)
            db.session.commit()
            
        return process


    def close_process(self, process):
        """
        set process to inactive
        """
        process.active = False
        db.session.commit()
 
                
    def process_locked(self, process):
        """
        check if a process is in a completed state, but is waiting
        for wait_time to expire
        """
        if not process.on_datetime or not process.off_datetime:
            return False

        return True

    
    def process_expired(self, process, 
                        now=datetime.datetime.now().replace(second=0, 
                                                            microsecond=0)):
        """
        check if a process is completed, and wait_time expired
        """
        start = None
        exptime = None
        if not process.on_datetime or not process.off_datetime:
            return False
        
        if process.on_datetime > process.off_datetime:
            start = process.on_datetime
        else:
            start = process.off_datetime
        
        exptime = start + datetime.timedelta(
            minutes=process.action.wait_minutes)
        
        if now >= exptime:
            return True
        
        return False

        
    def meets_condition(self, value, condition, threshold):
        if re.search(r'ge', condition, re.IGNORECASE):
            if value >= threshold:
                return True
        elif re.search(r'le', condition, re.IGNORECASE):
            if value <= threshold:
                return True
        elif re.search(r'gt', condition, re.IGNORECASE):
            if value > threshold:
                return True
        elif re.search(r'lt', condition, re.IGNORECASE):
            if value < threshold:
                return True
        elif re.search(r'eq', condition, re.IGNORECASE):
            if value == threshold:
                return True
    
        return False

              
    def handle_action_measurement(self, action, measurement):
        trigger = self.measurement_tripped(action, measurement)
        if trigger is None:
            return
        
        process = self.get_process(action, trigger)
        if not process:
            return
        
        if self.process_locked(process):
            if self.process_expired(process):
                # close this one down, and get a fresh one
                self.close_process(process)
                process = self.get_process(action, trigger)
                if not process:
                    return
            else:
                # an active process is still in progress. do nothing
                return
        
        if trigger == 'on' and process.on_datetime is not None:
            # this process already triggered 'on', now we will only 
            # accept 'off' option. skip
                return
        
        # SMS-MESSAGE action handler
        if re.search('sms', action.action_type, re.IGNORECASE):
            process.assign_datetime('on_datetime', datetime.datetime.now())
            process.assign_datetime('off_datetime', datetime.datetime.now())
            process.on_trigger = "%d-%s-%d" % (
                measurement.value, 
                action.on_condition, 
                action.on_threshold)
            db.session.commit()
            self.action_message(action, measurement)
            
        # SWITCH-OUTLET action handler
        elif re.search('switch', action.action_type, re.IGNORECASE):
            process.assign_datetime("%s_datetime" % trigger,
                                    datetime.datetime.now())
            setattr(process, "%s_trigger" % trigger, "%d-%s-%d" % (
                    measurement.value,
                    getattr(action, "%s_condition" % trigger),
                    getattr(action, "%s_threshold" % trigger)
                )
            )
            db.session.commit()
            
            # set state of an Outlet
            if trigger == 'on':
                rval = action.outlet.on()
            else:
                rval = action.outlet.off()
            
    
    def action_message(self, action, measurement):
        m = Messenger()

        body = "environment alert: %s is %s" % (
                measurement.measurement_type.name,
                measurement.text)

        try:
            rval = m.message(action.sms_recipient, body)
        except Exception as x:
            raise x

           
    def measurement_tripped(self, action, measurement):
        """
        does this measurement trigger one of the conditions of an action?
        """
        if re.search('sms', action.action_type, re.IGNORECASE):
            if self.meets_condition(measurement.value, 
                                        action.on_condition, 
                                        action.on_threshold):
                return 'on'
            
        elif re.search('switch', action.action_type, re.IGNORECASE):
            if self.meets_condition(measurement.value, 
                                        action.on_condition, 
                                        action.on_threshold):
                return 'on'
            
            elif self.meets_condition(measurement.value, 
                                        action.off_condition, 
                                        action.off_threshold):
                return 'off'
            
        return None
        
        
        
        
        
        
            

