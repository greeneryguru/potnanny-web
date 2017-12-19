#!/usr/bin/python3


"""

check latest db measurements and see if actions need to be taken.

"""

import os
import sys
import re
import time
import datetime
import logging
sys.path.append( os.environ.get('GREENERY_WEB','/var/www/greenery') )
from greenery import db
from greenery.apps.action.models import Action, ActionProcess
from greenery.apps.outlet.models import Outlet
from greenery.apps.measurement.models import MeasurementType, Measurement
from greenery.apps.admin.models import Setting
from greenery.lib.messenger import Messenger


logfile = '/var/tmp/greenery.errors.log'
logging.basicConfig(
    filename=logfile,
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',    
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('actions')
pause_seconds = 30


def main():
    now = datetime.datetime.now().replace(second=0, microsecond=0)
    poll = Setting.query.filter(Setting.name == 'polling interval minutes').first()
    if not poll:
        logger.error("could not determine polling interval from db")
        sys.stderr.write("error\n")
        sys.exit(1)

    if now.minute % poll.value:
        # now is not the right time to be running this
        sys.exit(0)
    else:
        then = now - datetime.timedelta(minutes=poll.value)
        actions = actions = Action.query.filter(
            Action.enabled == True
        ).all()
        if not actions:
            sys.exit(0)

        # pause, to let any polling jobs finish, before we begin
        time.sleep(pause_seconds)

        processes = open_processes(now)
        for a in actions:
            process_action(a, then, now, processes)

        sys.exit(0)
        

def process_action(action, then, now, processes):
    measurements = Measurement.query.filter(
        Measurement.type_id == action.measurement_id,
        Measurement.date_time.between(then,now)
    ).all()

    if not measurements:
        return

    my_process = None
    if processes:
        for p in processes:
            if p.action_id == action.id:
                my_process = p
                break

    for m in measurements:
        if re.search('sms', action.action_type, re.IGNORECASE):
            trigger = meets_condition(m.value, action.on_condition, 
                                        action.on_threshold)
            if my_process:
                return

            rval = sms_message(action, m)
            if not rval:
                ap = ActionProcess(action.id)
                ap.active = True
                ap.on_datetime = now
                ap.on_trigger = "%d-%s-%d" % (m.value, action.on_condition, 
                                                action.on_threshold)  
                db.session.add(ap)
                db.session.commit()
                processes.append(ap)
            else:
                # sms error message here!
                pass

            return 

        if re.search('switch', action.action_type, re.IGNORECASE):
            trigger = meets_condition(m.value, action.on_condition, 
                                        action.on_threshold)
            if trigger:
                if my_process:
                    if not my_process.on_datetime:
                        my_process.on_datetime = now
                        my_process.on_trigger = "%d-%s-%d" % (m.value, 
                                                    action.on_condition, 
                                                    action.on_threshold) 
                        db.session.commit()
                        return 
                else:
                    my_process = ActionProcess(action.id)
                    my_process.active = True
                    my_process.on_datetime = now
                    my_process.on_trigger = "%d-%s-%d" % (m.value, 
                                                    action.on_condition, 
                                                    action.on_threshold)  
                    db.session.add(my_process)
                    db.session.commit()
                    processes.append(my_process)
                    return

            trigger = meets_condition(m.value, action.off_condition, 
                                        action.off_threshold)
            if trigger:
                if my_process:
                    if not my_process.on_datetime:
                        my_process.off_datetime = now
                        my_process.off_trigger = "%d-%s-%d" % (m.value, 
                                                    action.off_condition, 
                                                    action.off_threshold) 
                        db.session.commit()
                        return 
                else:
                    my_process = ActionProcess(action.id)
                    my_process.active = True
                    my_process.off_datetime = now
                    my_process.off_trigger = "%d-%s-%d" % (m.value, 
                                                    action.off_condition, 
                                                    action.off_threshold)  
                    db.session.add(my_process)
                    db.session.commit()
                    processes.append(my_process)
                    return

def outlet_switch(action, state):
    if state:
        rval = action.outlet.on()
    else:
        rval = action.outlet.off()

    if rval['state'] != state:
        logger.warning("outlet to state '%d' failed with code: %s\n" % (state, rval))
        return

    db.session.commit()
    return


def sms_message(action, measurement):
    m = Messenger()

    body = "GREENERY.GURU: %s is %s" % (
                measurement.measurement_type.name,
                measurement.text)

    try:
        rval = m.message(action.sms_recipient, body)
    except Exception as x:
        logger.error("sms message send failed: %s" % x)




"""
compare a value to a threshold based on a condition (gt|lt|le|ge|eq)

params:
    - a number (int)
    - a condition (str) (gt|lt|eq...)
    - a threshold value (int)
returns:
   True or False
"""
def meets_condition(value, condition, threshold):
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


"""
Get list of any active ActionProcess objects

params:
    a datetime obj
returns:
    a list of ActionProcess objects
"""
def open_processes(now):
    mylist = []

    action_processes = ActionProcess.query.filter(
        ActionProcess.active == True
    ).all()

    if not action_processes:
        return mylist

    for a in action_processes:
        if actionprocess_check(a, now):
            mylist.append(a) 
           
    return mylist


"""
Check status of an action process, see if it is still active and valid.
Shut the process down if it is expired.

params:
    - an ActionProcess object
    - a datetime obj

returns:
    True if the ActionProcess is still active and valid
    False if the ActionProcess has been closed, and is not longer active
""" 
def actionprocess_check(ap, now):             
    if re.search(r'sms', ap.action.action_type, re.IGNORECASE):
        if ap.on_datetime:
            then = ap.on_datetime + datetime.timedelta(minutes=ap.action.wait_minutes)
            if now > then:
                ap.active = False
                db.session.commit()
                return False
            else:
                return True
        else:
            return False

    elif re.search(r'switch', ap.action.action_type, re.IGNORECASE):
        if not ap.on_datetime or not ap.off_datetime:
            return True

        dt = None
        if ap.on_datetime > ap.off_datetime:
            dt = ap.on_datetime
        else:
            dt = ap.off_datetime

        then = dt + datetime.timedelta(minutes=ap.action.wait_minutes)
        if now > then:
            ap.active = False
            db.session.commit()
            return False
        else:
            return True
        
    return False



if __name__ == '__main__':
    main()

