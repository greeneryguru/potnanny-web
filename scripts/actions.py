#!/usr/bin/python3

#
# check latest db measurements and see if actions need to be taken
#
#

import os
import sys
import re
import datetime
import logging
sys.path.append( os.environ.get('GREENERY_WEB','/var/www/greenery') )
from app import db
from app.actions.models import Action, ActionProcess
from app.outlet.models import Outlet
from app.measurement.models import MeasurementType, Measurement
from app.admin.models import Setting


logging.basicConfig(filename='/var/tmp/greenery.actions.log')
logger = logging.getLogger('actions')


def main():
    now = datetime.datetime.now()
    poll = Setting.query.filter(Setting.name == 'polling interval minutes').first()
    
    if now.minute % poll.value:
        # not the right time to be running this
        sys.exit(0)
    else:
        # let any polling jobs finish before we start handling records
        time.sleep(25)

    actions = Action.query.all()
    for a in actions:
        recent = Measurement.query.filter(Measurement.type_id == a.type_id).order_by(Measurement.date_time.desc()).first()
        rval = action_needed(a, now, recent)
        if rval and a.action == 'switch-outlet':
            outlet_switch(a)
        elif rval and a.action == 'sms-message':
            sms_message(a, recent)
           
   
def outlet_switch(action):
    o = Outlet.query.filter(Outlet.name == action.action_target).first()
    if action.action_state == 0:
        rval = o.off()
        if not rval:
            o.state = 0
    else:
        rval = o.on()
        if not rval:
            o.state = 1

    db.session.commit()


def sms_message(action, measurement):
    pass


def action_needed(action, now, meas):
    trigger = False
    past = now - datetime.timedelta(minutes = action.wait_time)

    if action.condition == 'GT' and meas.value > action.value:
        trigger = True
    elif action.condition == 'LT' and meas.value < action.value:
        trigger = True
    elif action.condition == 'EQ' and meas.value == action.value:
        trigger = True

    if not trigger:
        return false

    procs = ActionProcess.query.filter(ActionProcess.action_id == a.id)
    nprocs = len(procs)
    removed = 0
    for p in procs:
        if p.date_time < past:
            db.session.delete(p)
            removed += 1

    db.session.commit()
    if nprocs == removed:
        return True

    return False


if __name__ == '__main__':
    main()

