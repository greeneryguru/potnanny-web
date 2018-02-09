#!/usr/bin/env python3


"""

Poll bluetooth sensors for data
"""

import os
import sys
import re
import time
import datetime
import json
from aifc import data
sys.path.append( os.environ.get('FLASK_APP','/var/www/potnanny') )
from potnanny.application import create_app
from potnanny.extensions import db
from potnanny.apps.measurement.models import Measurement
from potnanny.apps.settings.models import Setting
from potnanny.apps.sensor.models import Sensor
from miflora.miflora_poller import MiFloraPoller
from miflora.backends.bluepy import BluepyBackend
from miflora.miflora_poller import MiFloraPoller, \
    MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from miflora import miflora_scanner, BluepyBackend



# global vars
now = datetime.datetime.now().replace(second=0, microsecond=0)
sensor_file = '/var/tmp/btle-sensors.json'

def main():
    known_sensors = {}
    devices = None
    
    if not os.path.exists(sensor_file):
        sys.stderr.write("sensor file '%' does not exist\n" % sensor_file)
        sys.exit(1)
        
    with open(sensor_file, 'r') as fh:
        devices = json.load(fh)
    
    for addr, name in devices.items():
        if addr not in known_sensors:
            known_sensors[addr] = sensor_id(addr, name)
            
        if re.search(r'flower care|mate', name, re.IGNORECASE):
            rval = flower_care(addr)
            # print(rval)
        
        
    


def flower_care(address):
    readings = {
        'temperature': MI_TEMPERATURE,
        'soil-moisture': MI_MOISTURE,
        'ambient-light': MI_LIGHT,
        'soil-fertility': MI_CONDUCTIVITY,
        'battery': MI_BATTERY,
    }
    data = {
        'name': None,
        'address': address,
        'measurements': {},
    }
    poller = MiFloraPoller(address, BluepyBackend)
    data['name'] = poller.name()
    
    for key, value in readings.items():
        result = poller.parameter_value(value)
        if result is not None:
            data['measurements'][key] = result
            obj = Measurement(address, key, result, now)
            db.session.add(obj)
    
    db.session.commit()
    return data


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


