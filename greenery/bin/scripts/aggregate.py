#!/usr/bin/python3


"""

aggregate previous-hours measurements into avg/min/max and insert to 
MeasurementAverage objects.

"""

import os
import sys
import re
import time
import datetime
import logging
sys.path.append( os.environ.get('GREENERY_WEB','/var/www/greenery') )
from greenery import db
from greenery.apps.measurement.models import Measurement, MeasurementAverage
from greenery.apps.sensor.models import Sensor


logfile = '/var/tmp/greenery.errors.log'
logging.basicConfig(filename=logfile)
logger = logging.getLogger('actions')
logger.setLevel(10)


def main():
    now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    then = now - datetime.timedelta(hours=1)

    sensors = Sensor.query.all()
    for s in sensor:
        tally = 0
        avg = None        
        nmin = None
        nmax = None
        results = Measurement.query.filter(Measurement.sensor_id == s.id).filter(Measurement.date_time.between(then, now))
        if not results:
            continue

        for r in results:
            # max
            if not nmax:
                nmax = r.value
            else:
                if r.value > nmax:
                    nmax = r.value
            
            # min
            if not nmin:
                nmin = r.value
            else:
                if r.value < nmin:
                    nmin = r.value

            tally += r.value

        avg = tally/len(results)
        m = MeasurementAverage(s.id, avg, nmin, nmax, then)
        db.session.add(m)

    db.session.commit()


if __name__ == '__main__':
    main()

