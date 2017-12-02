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
from greenery.apps.action.models import Action, ActionProcess, ActionTrigger
from greenery.apps.outlet.models import Outlet
from greenery.apps.measurement.models import MeasurementType, Measurement
from greenery.apps.admin.models import Setting
from greenery.apps.sensor.models import Sensor
from greenery.lib.messenger import Messenger


logfile = '/var/tmp/greenery.errors.log'
logging.basicConfig(filename=logfile)
logger = logging.getLogger('actions')
logger.setLevel(10)
pause_time = 15


def main():
    now = datetime.datetime.now()
    poll = Setting.query.filter(Setting.name == 'polling interval minutes').first()
    if not poll:
        logger.error("could not determine polling interval from db")
        sys.stderr.write("error\n")
        sys.exit(1)

    if now.minute % poll.value:
        # not the right time to be running this
        sys.exit(0)
    else:
        # pause, to let any polling jobs finish, before we begin
        time.sleep(pause_time)
        sys.exit(process_actions(now, poll.value))


"""
process any actions for the latest measurements

params:
    1. datetime.datetime
    2. the system polling inverval (int)

returns:
    0 on success, non-zero on failure
"""
def process_actions(now, poll_interval):
    actions = Action.query.all()
    for a in actions:
        measurements = latest_measurements(a.type_id, now, poll_interval)
        if not measurements:
            continue

        for m in measurements:
            rval = is_action_needed(a, now, m)
            if rval:
                t = ActionTrigger(a.id, now, "sensor='%s', value=%s, thresh='%s %d', action='%s %s %d'" % (m.sensor, m.value, a.condition, a.value, a.action, a.action_target, a.action_state))
                p = ActionProcess(a.id, now)

                db.session.add(t)
                db.session.add(p)
                db.session.commit()

                if a.action == 'switch-outlet':
                    outlet_switch(a)
                elif a.action == 'sms-message':
                    sms_message(a, m)
   
    return 0        


"""
get latest measurement for particular measurement-type

params:
    1. a MeasurementType id
    2. datetime.datetime
    3. system polling interval
returns:
    a list of Measurement object on success. None on fail
"""
def latest_measurements(id, now, poll_interval):
    add_buffer = 1
    past = now - datetime.timedelta(minutes=poll_interval + add_buffer)
    mt = MeasurementType.query.get(id)

    dat = Measurement.query.filter(Measurement.code == mt.code, Measurement.date_time > past).all()

    return dat


def outlet_switch(action):
    o = Outlet.query.filter(Outlet.name == action.action_target).first()
    if not o:
        logger.warning("no outlet with name '%s' found" % action.action_target)
        return

    if action.action_state == 0:
        rval = o.off()
    else:
        rval = o.on()

    if not rval:
        o.state = action.action_state
        db.session.commit()
    else:
        logger.warning("outlet on/off failed with code: %d\n" % rval)

    return


def sms_message(action, measurement):
    m = Messenger()
    code = 'temperature'
    if measurement.code == 'h':
        code = 'humidity' 
    elif measurement.code == 'sm':
        code = 'soil moisture'

    body = "GREENERY.GURU: sensor '%s' %s is %d" % (measurement.sensor, code, measurement.value)
    if code == 'temperature':
        body += ' degrees'
    elif code == 'humidity' or code == 'soil moisture':
        body += ' percent'

    try:
        rval = m.message(action.action_target, body)
    except Exception as x:
        logger.error("sms message send failed: %s" % x)


"""
check if an action needs to be run, based on current related measurement data.

params:
    1. an Action object
    2. datetime.datetime
    3. a Measurement object

returns:
    True/False
"""
def is_action_needed(action, now, meas):
    trigger = False
    past = now - datetime.timedelta(minutes = action.wait_time)

    if action.condition == 'GT' and meas.value > action.value:
        trigger = True
    elif action.condition == 'LT' and meas.value < action.value:
        trigger = True
    elif action.condition == 'EQ' and meas.value == action.value:
        trigger = True

    if not trigger:
        return False

    # check if this action already has a waiting process that needs to time out
    procs = ActionProcess.query.filter(ActionProcess.action_id == action.id)
    for p in procs:
        if p.date_time < past:
            # delete stale processes
            db.session.delete(p)
            db.session.commit()
        else:
            return False

    return True


if __name__ == '__main__':
    main()

