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
from greenery.apps.measurement.models import Measurement, MeasurementType, MeasurementAverage
from greenery.apps.sensor.models import Sensor


logfile = '/var/tmp/greenery.errors.log'
logging.basicConfig(filename=logfile)
logger = logging.getLogger('actions')
logger.setLevel(10)


def main():
    now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    then = now - datetime.timedelta(hours=1)

    mtypes = MeasurementType.query.all()
    for mt in mtypes:
        ids = sensors_reporting_in_range(mt.id, then, now)
        if not ids:
            continue

        sensors = Sensor.query.filter(
            Sensor.id.in_(ids)
        ).all()

        for s in sensors:
            tally = 0
            avg = None        
            nmin = None
            nmax = None
            results = Measurement.query.filter(
                Measurement.type_id == mt.id,
                Measurement.sensor_id == s.id
            ).filter(
                Measurement.date_time.between(then, now)
            ).all()

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

            # averages are rounded to only on decimal place accuracy
            avg = round(tally/len(results), 1)
            m = MeasurementAverage(mt.id, s.id, avg, nmin, nmax, then)
            db.session.add(m)

        db.session.commit()


def sensors_reporting_in_range(pk, then, now):
    data = []
    results = Measurement.query.filter(
        Measurement.type_id == pk,
        Measurement.date_time.between(then,now)
    ).order_by(
        Measurement.sensor_id
    ).group_by(
            Measurement.sensor_id
    ).distinct(
        Measurement.sensor_id
    ).all()
    for r in results:
        data.append(r.sensor_id)

    return data


if __name__ == '__main__':
    main()

