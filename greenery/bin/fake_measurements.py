#!/usr/bin/python3

#
# inserts new random temp and humidity measurements into
# the table every minute
#
#

import os
import sys
import re
import time
import datetime
import random
sys.path.append( os.environ.get('GREENERY_WEB','/var/www/greenery') )
from greenery import db
from greenery.apps.measurement.models import MeasurementType, Measurement
from greenery.apps.sensor.models import Sensor

def main():
    fahrenheit = True
    now = datetime.datetime.now().replace(second=0, microsecond=0)
    mtypes = MeasurementType.query.all()
    sensors = Sensor.query.all()
    for s in sensors:
        tid = None

        if re.search(r'temp', s.tags):
            tid = match_names('temp', mtypes)
            if not tid:
                continue
            val = random.randint(72, 79)
            
            m1 = Measurement(tid, s.id, val, u'%d\N{DEGREE SIGN}F' % val, now)
            db.session.add(m1)

        if re.search(r'soil', s.tags):
            tid = match_names('soil', mtypes)
            if not tid:
                continue
            val = random.randint(28,34)
            m2 = Measurement(tid, s.id, val, "%d%%" % val, now)
            db.session.add(m2)

        if re.search(r'humid', s.tags):
            tid = match_names('humid', mtypes)
            if not tid:
                continue
            val = random.randint(40,50)
            m3 = Measurement(tid, s.id, val, "%d%%" % val, now)
            db.session.add(m3)
      
        db.session.commit()
        

def match_names(txt, obj):
    for o in obj:
        if re.search(txt, o.name):
            return o.id
        
    return None
if __name__ == '__main__':
    main()

