#!/usr/bin/python3


"""

Clean up database of old measurements.

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
from greenery.apps.admin.models import Setting


logfile = '/var/tmp/greenery.errors.log'
logging.basicConfig(filename=logfile)
logger = logging.getLogger('actions')
logger.setLevel(10)


def main():
    now = datetime.datetime.now()
    hi_limit = Setting.query.filter(
            Setting.name == 'hi-res data retention days').first().value
    avg_limit = Setting.query.filter(
            Setting.name == 'hourly-avg data retention days').first().value

    
    # delete hi-resolution data over the limit
    results = Measurement.query.filter(
        Measurement.date_time < now - datetime.timedelta(days=hi_limit)
    ).delete()
    if results:
        logger.info("purge removed %d rows of hi-resolution measurements" % results)
        db.session.commit()
        

    # delete averaged data over the limit
    results = MeasurementAverage.query.filter(
        MeasurementAverage.date_time < now - datetime.timedelta(days=avg_limit)
    ).delete()
    if results:
        logger.info("purge removed %d rows of hourly-avg measurements" % results)
        db.session.commit()


if __name__ == '__main__':
    main()

