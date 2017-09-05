#!/usr/bin/python

""" 
create some test temperature/humidity data.

make sure there are two dummy sensors built in inventory first, with id's 
of 1 and 2.
"""

import os
import sys
import random
import datetime
import django.utils.timezone
sys.path.append('/home/jeff/Development/greenery')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greenery.settings')
django.setup()
from app.inventory.models import Sensor
from app.measurement.models import SensorData


def main():
    now = django.utils.timezone.now()
    for n in range(0,20):
        now = now - datetime.timedelta(minutes=5)
        s1 = Sensor.objects.get(id=1)
        s2 = Sensor.objects.get(id=2)
        for s in (s1, s2):
            temp = random.randint(60,80)
            humidity = random.randint(30,66)
            t = SensorData.objects.create(
                datetime=now,
                value=temp,
                sensor=s,
                data_type='t')
            t.save()

            h = SensorData.objects.create(
                datetime=now,
                value=humidity,
                sensor=s,
                data_type='h')
            h.save()

if __name__ == '__main__':
    main()
