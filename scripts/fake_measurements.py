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


def main():
    t = MeasurementType.query.filter(MeasurementType.name.contains('temp'))[0]
    h = MeasurementType.query.filter(MeasurementType.name.contains('humid'))[0]

    for i in range(0,10):
        now = datetime.datetime.now()
        m1 = Measurement(t.id, random.randint(65,85), now)
        db.session.add(m1)

        m2 = Measurement(h.id, random.randint(45,58), now)
        db.session.add(m2)

        db.session.commit()
        time.sleep(60)
        

if __name__ == '__main__':
    main()

