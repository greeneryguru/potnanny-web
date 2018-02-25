from potnanny.extensions import db
from potnanny.apps.measurement.models import Measurement
from potnanny.apps.outlet.models import Outlet
from potnanny.apps.messenger.models import Messenger
from potnanny.apps.sensor.models import Sensor
from potnanny.apps.outlet.models import Outlet
import datetime
import re


class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    measurement_type = db.Column(db.String(24), nullable=False)
    sensor_address = db.Column(db.String(24), nullable=False, unique=True)
    outlet_id = db.Column(db.String(128), nullable=True)
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
    

    def __init__(self, name, mid, oid, addr, atype):
        self.name = name
        self.measurement_type = mid
        self.outlet_id = oid
        self.sensor_address = addr
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
            'measurement_type': self.measurement_type,
            'outlet_id': self.outlet_id,
            'sensor_address': self.sensor_address,
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
    
    def __init__(self, celsius=True):
        self.celsius = celsius    
        self.actions = list(
            Action.query.filter(
                Action.active == True
            )
        )                
    
    
    """
    convert celsius to F
    """
    def c_to_f(self, c):
        return (9.0/5.0 * c) + 32
    
    
    """
    evaluate a measurement against all available actions to see if they are
    compatible/related.
    
    If they are related, the measurement will be evaluated against the action
    thresholds to see if any action is necessary.
    If so, an Action and ActionProcess will be initiated.
    
    params:
        a Measurement object
    returns:
        None
    """
    def eval_measurement(self, m):
        for action in self.actions:
            # evaluate measurement values against action criteria and skip
            # any pairs that are completely unrelated.
            if action.measurement_type != m.type_m:
                continue
            
            if action.sensor_address != 'any' and action.sensor_address != m.sensor:
                continue
            
            self.handle_measurement(action, m) 
            
          
    def handle_measurement(self, action, measurement):
        trigger = self.measurement_tripped(action, measurement)
        if not trigger:
            return
        
        process = self.get_process(action, trigger)
        if not process:
            return
            
        # SMS-MESSAGE action handler
        if re.search('sms', action.action_type, re.IGNORECASE):
            sensor = Sensor.query.filter(
                Sensor.address == measurement.sensor).first()
                
            mvalue = measurement.value
            if measurement.type_m == 'temperature' and not self.celsius:
                mvalue = self.c_to_f(mvalue)
                
            process.assign_datetime('on_datetime', datetime.datetime.now())
            process.assign_datetime('off_datetime', datetime.datetime.now())
            process.on_trigger = "%d-%s-%d" % (
                mvalue, 
                action.on_condition, 
                action.on_threshold)
            db.session.commit()
            self.action_message(action, sensor.name, measurement.type_m, mvalue)
            
        # SWITCH-OUTLET action handler
        elif re.search('switch', action.action_type, re.IGNORECASE):
            mvalue = measurement.value
            if measurement.type_m == 'temperature' and not self.celsius:
                mvalue = self.c_to_f(mvalue)
                
            process.assign_datetime("%s_datetime" % trigger,
                                    datetime.datetime.now())
            setattr(process, "%s_trigger" % trigger, "%d-%s-%d" % (
                    mvalue,
                    getattr(action, "%s_condition" % trigger),
                    getattr(action, "%s_threshold" % trigger)
                )
            )
            db.session.commit()
            
            # set state of an Outlet
            try:
                outlet = Outlet.query.get(int(action.outlet_id))
                if trigger == 'on':
                    rval = outlet.on()
                else:
                    rval = outlet.off()
            except Exception as x:
                raise x
            
            
    def get_process(self, action, trigger):
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
        need_new = False
        
        process = ActionProcess.query.filter(
            ActionProcess.active == True,
            ActionProcess.action_id == action.id
        ).first()
    
        if process:
            if self.process_locked(process):
                if self.process_expired(process):
                    # close this one down, and get a fresh one
                    self.close_process(process)
                else:
                    return None
            else:
                if getattr(process, "%s_datetime" % trigger) is not None:
                    # the trigger we are dealing with has already been set
                    # in this process. we cant re-use it.
                        return None
                
                return process    
            
        
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
        check if a process is in an incomplete state
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

    
    def action_message(self, action, sensor, measurement, value):
        m = Messenger()

        body = "environment alert: sensor '%s' %s is %d" % (
                sensor, measurement, value)

        try:
            rval = m.message(action.sms_recipient, body)
        except Exception as x:
            raise x

           
    def measurement_tripped(self, action, measurement):
        """
        does this measurement trigger one of the conditions of an action?
        """
        mvalue = measurement.value
        if measurement.type_m == 'temperature' and not self.celsius:
            mvalue = self.c_to_f(mvalue)
            
        if re.search('sms', action.action_type, re.IGNORECASE):
            if self.meets_condition(mvalue, 
                                        action.on_condition, 
                                        action.on_threshold):
                return 'on'
            
        elif re.search('switch', action.action_type, re.IGNORECASE):
            if self.meets_condition(mvalue, 
                                        action.on_condition, 
                                        action.on_threshold):
                return 'on'
            
            elif self.meets_condition(mvalue, 
                                        action.off_condition, 
                                        action.off_threshold):
                return 'off'
            
        return None
        
        
        
        
        
        
            

