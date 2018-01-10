#!/usr/bin/env python3

"""

inserts fake random measurements into tables

"""

import os
import sys
import re
import datetime
import random
sys.path.append( os.environ.get('FLASK_APP','/var/www/potnanny') )
from potnanny.application import create_app
from potnanny.extensions import db
from potnanny.apps.measurement.models import MeasurementType, Measurement
from potnanny.apps.sensor.models import Sensor

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
    app = create_app()
    app.app_context().push()
    main()

