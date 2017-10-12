#!/usr/bin/python3

#
# Runs for a while, and inserts new random temp and humidity measurements into
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
from app import db
from app.measurement.models import MeasurementType, Measurement
from app.sensor.models import Sensor

def main():
    now = datetime.datetime.now().replace(second=0, microsecond=0)
    sensors = Sensor.query.all()
    for s in sensors:
        dat = s.test_data()
        for k, v in dat.items():
            m = Measurement(s.id, k, v, now)
            db.session.add(m)

    db.session.commit()
        

if __name__ == '__main__':
    main()

