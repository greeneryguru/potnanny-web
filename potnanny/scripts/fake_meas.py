#!/usr/bin/env python3


"""

Create fake sensors data.

"""

import os
import sys
import re
import time
import datetime
import json
import random
sys.path.append( os.environ.get('FLASK_APP','/var/www/potnanny') )
from potnanny.application import create_app
from potnanny.extensions import db
from potnanny.apps.measurement.models import Measurement
from potnanny.apps.settings.models import Setting
from potnanny.apps.sensor.models import Sensor


# global vars
now = datetime.datetime.now().replace(second=0, microsecond=0)

def main():
    sensors = Sensor.query.all()  
    for sensor in sensors:
        flower_care(sensor.address)
        
    
"""
Poll a Mi Flower Care bluetooth sensor for data.

params:
    a device address
returns:
    a list of Measurment objects
    
"""
def flower_care(address):
    count = 0
    measurements = []
    readings = {
        'temperature': random.randint(18,23),
        'soil-moisture': random.randint(12,20),
        'ambient-light': random.randint(9000,11000),
        'soil-fertility': random.randint(200,500),
        'battery': random.randint(25,100),
    }
    
    for key, value in readings.items():
        obj = Measurement(address, key, value, now)
        db.session.add(obj)
        measurements.append(obj)

    db.session.commit()
    
    return
    

if __name__ == '__main__':
    
    app = create_app()
    app.app_context().push()
    
    poll = Setting.query.get(1)

    if not poll:
        # logger.error("could not determine polling interval from db")
        sys.stderr.write("error. could not determine polling interval from db\n")
        sys.exit(1)

    if now.minute % poll.interval > 0:
        # not the right time to be running this. exit
        sys.exit(0)

    main()


