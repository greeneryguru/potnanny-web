#!/usr/bin/python

import os
import sys
import re
import django.utils.timezone
sys.path.append(os.getenv('GREENERY_WEB'))
django.setup()
from app.inventory.models import Sensor
from app.measurement.models import SensorData


def main():
    now = django.utils.timezone.now()
    try:
        sensors = Sensor.objects.filter(active=True)
        for s in sensors:
            if re.search(r'temphumid', s.sensor_type, re.IGNORECASE):
                collect_temphumid(s, now)
                continue
            if re.search(r'^temp$', s.sensor_type, re.IGNORECASE):
                collect_temp(s, now)
                continue
                
    except:
    

def collect_temphumid(sensor, dt):
    if re.search(r'DHT', sensor.device, re.IGNORECASE):
        try:
            h, t = read_dht(sensor, dt)
            hum = SensorData.object.create(sensor=sensor,
                datetime=dt,
                data_type='h',
                value=h)
            hum.save()

            temp = SensorData.object.get_or_create(sensor=sensor,
                datetime=dt,
                data_type='t',
                value=t)
            temp.save()
            return True
        except:
            pass

    
def read_dht(sensor):
    pin = sensor.gpio

    # Validate pin is a valid GPIO.
    if pin is None or int(pin) < 0 or int(pin) > 31:
        raise ValueError('Pin must be a valid GPIO number 0 to 31.')
    # Get a reading from C driver code.
    result, humidity, temp = driver.read(sensor, int(pin))
    if result in common.TRANSIENT_ERRORS:
        # Signal no result could be obtained, but the caller can retry.
        return (None, None)
    elif result == common.DHT_ERROR_GPIO:
        raise RuntimeError('Error accessing GPIO.')
    elif result != common.DHT_SUCCESS:
        # Some kind of error occured.
        raise RuntimeError('Error calling DHT test driver read: {0}'.format(result))

    return (humidity, temp)

if __name__ == '__main__':
    main()
