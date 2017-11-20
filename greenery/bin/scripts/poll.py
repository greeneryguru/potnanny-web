#!/usr/bin/python3


"""

Poll sensors to get temp/humid/soil-moisture etc...

"""

import os
import sys
import re
import time
import datetime
import logging
sys.path.append( os.environ.get('GREENERY_WEB','/var/www/greenery') )
from greenery import db
from greenery.lib.sensors import OneWireTemp
from greenery.apps.measurement.models import MeasurementType, Measurement
from greenery.apps.admin.models import Setting
from greenery.apps.sensor.models import Sensor


logfile = '/var/tmp/greenery.errors.log'
logging.basicConfig(filename=logfile)
logger = logging.getLogger('actions')
logger.setLevel(10)


def main():
    now = datetime.datetime.now().replace(second=0, microsecond=0)
    poll = Setting.query.filter(Setting.name == 'polling interval minutes').first()
    
    if not poll:
        logger.error("could not determine polling interval from db")
        sys.stderr.write("error\n")
        sys.exit(1)

    if now.minute % poll.value:
        # not the right time to be running this
        sys.exit(0)
    else:
        fahrenheit = bool(Setting.query.filter(Setting.name == 'store temperature fahrenheit').first().value)

        # poll the devices
        sensors = Sensor.query.all()
        for s in sensors:
            results = None
            if re.search(r'28-\d+', s.notes):
                obj = OneWireTemp(s.notes)
                results = obj.get_temp(fahrenheit)
            
            if not results:
                continue 

            if type(results) is list:
                for r in results:
                    m = Measurement(s.id, r['type'], r['value'], now)
                    db.session.add(m)
            else:
                m = Measurement(s.id, results['type'], results['value'], now)
                db.session.add(m)

            db.session.commit()
 

if __name__ == '__main__':
    main()

