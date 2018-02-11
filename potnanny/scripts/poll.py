#!/usr/bin/env python3


"""

Poll bluetooth sensors for data.
Also, check any new measurements that come in to see if they need actions.

"""

import os
import sys
import re
import time
import datetime
import json
sys.path.append( os.environ.get('FLASK_APP','/var/www/potnanny') )
from potnanny.application import create_app
from potnanny.extensions import db
from potnanny.apps.measurement.models import Measurement
from potnanny.apps.settings.models import Setting
from potnanny.apps.vesync.models import VesyncManager
from potnanny.apps.sensor.models import Sensor
from potnanny.apps.action.models import Action, ActionProcess, ActionManager
from miflora.backends.bluepy import BluepyBackend
from miflora.miflora_poller import MiFloraPoller
from miflora.miflora_poller import MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, \
    MI_TEMPERATURE, MI_BATTERY



# global vars
now = datetime.datetime.now().replace(second=0, microsecond=0)
sensor_file = '/var/tmp/btle-sensors.json'

def main():
    known_sensors = {}
    devices = None
    measurement_queue = []
    
    if not os.path.exists(sensor_file):
        sys.stderr.write("sensor file '%' does not exist\n" % sensor_file)
        sys.exit(1)
        
    with open(sensor_file, 'r') as fh:
        devices = json.load(fh)
    
    for addr, name in devices.items():
        if addr not in known_sensors:
            known_sensors[addr] = sensor_id(addr, name)
            
        if re.search(r'flower care|mate', name, re.IGNORECASE):
            results = flower_care(addr)
            if results:
                measurement_queue += results
        

    # send all measurements that came in, off to be checked for needed actions
    mgr = ActionManager()
    for m in measurement_queue:
        mgr.handle_measurement(m)
        
    
"""
Poll a Mi Flower Care bluetooth sensor for data.

params:
    a device address
returns:
    a list of Measurment objects
    
"""
def flower_care(address):
    measurements = []
    readings = {
        'temperature': MI_TEMPERATURE,
        'soil-moisture': MI_MOISTURE,
        'ambient-light': MI_LIGHT,
        'soil-fertility': MI_CONDUCTIVITY,
        'battery': MI_BATTERY,
    }
    poller = MiFloraPoller(address, BluepyBackend)
    data['name'] = poller.name()
    
    for key, value in readings.items():
        result = poller.parameter_value(value)
        if result is not None:
            obj = Measurement(address, key, result, now)
            db.session.add(obj)
            measurements.append(obj)
    
    db.session.commit()
    return measurements


def sensor_id(addr, name):
    s = Sensor.query.filter(
        Sensor.address == addr
    ).first()
    if s:
        return s.id
    
    obj = Sensor(name, addr)
    db.session.add(obj)
    db.session.commit()
    return obj.id
    

if __name__ == '__main__':
    
    app = create_app()
    app.app_context().push()
    
    poll = Setting.query.filter(
        Setting.name == 'polling interval minutes'
    ).first()

    if not poll:
        # logger.error("could not determine polling interval from db")
        sys.stderr.write("error. could not determine polling interval from db\n")
        sys.exit(1)

    if now.minute % poll.value > 0:
        # not the right time to be running this. exit
        sys.exit(0)

    main()


