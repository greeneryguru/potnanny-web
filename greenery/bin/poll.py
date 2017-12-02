#!/usr/bin/python3


"""

Poll sensors to get temp/humid/soil-moisture etc...

The Arduino accepts number-based command codes over the usb serial connection.
Like,
    
    002\n   = 0=mode(get),0=measurement(temperature),2=address(digital pin 2)
    0214\n  = 0=mode(get),2=measurement(soil),14=address(analog pin 14, or A0)

Commands MUST be terminated with '\n'!

See command-map in global vars

"""

import os
import sys
import re
import time
import datetime
import logging
import serial
sys.path.append( os.environ.get('GREENERY_WEB','/var/www/greenery') )
from greenery import db
from greenery.apps.measurement.models import MeasurementType, Measurement
from greenery.apps.admin.models import Setting
from greenery.apps.sensor.models import Sensor


logfile = '/var/tmp/greenery.errors.log'
logging.basicConfig(filename=logfile)
logger = logging.getLogger('actions')
logger.setLevel(10)


# global vars
poll = None
fahrenheit = None
sdevice = '/dev/ttyUSB0'
now = datetime.datetime.now().replace(second=0, microsecond=0)

cmd_map = {
    # first char
    'get':          0,
    'set':          1,
    'tx':           2,

    # second(*) char for get-mode
    'temperature':  0,
    'humidity':     1,
    'soil':         2,
}


def main():
    ser = None

    try:
        ser = serial.Serial(sdevice, 9600, 5)
    except Exception as x:
        logger.error(x)
        sys.stderr.write("Error! see log %s\n" % logfile)
        sys.exit(1)

    mtypes = MeasurementType.query.all()
    sensors = Sensor.query.all()
    for s in sensors:
        for typ in ('temperature', 'humidity', 'soil'):
            if re.search(typ, s.tags):
                cmd = "%d%d%d\n" % (cmd_map['get'], cmd_map[typ], s.address)
                ser.write(cmd.encode('UTF-8'))
                while True:
                    # returns like; 
                    #   line = "sm,14,22" (code, address, value)
                    line = ser.readline()
                    print(line)
                    if re.search(r'^ok', line, re.IGNORECASE):
                        # nothing more to read!
                        break;
                    if re.search(r'^fail', line, re.IGNORECASE):
                        logger.warning("sensor '%s' fail result '%s'" % (s.name, line))
                        break;
                    
                    atoms =  line.split(",")
                    if len(atoms) != 3:
                        logger.warning("sensor '%s' garbled output '%s" % (s.name, line))
                        continue;

                    code,addr,val = atoms
                    mt = match_flag_to_object(code, mtypes)
                    if code == 't' and fahrenheit:
                        val = val * 1.8 + 32

                    label = format_label(code, val, fahrenheit)

                    # adjust for only one decimal place during write to db
                    m = Measurement(mt.id, s.id, "%0.1f" % float(val), label, now)
                    db.session.add(m)

        db.session.commit()

    ser.close()


def match_flag_to_object(f, objects):
    label = None

    if f == 't':
        label = 'temperature'
    elif f == 'h':
        label = 'humidity'
    elif f == 'sm':
        label = 'soil moisture'
    else:
        return None

    for o in objects:
        if o.name == label:
            return o

    return None


def format_label(typ, val, fahrenheit=False):
    if re.search(r'^t', typ):
        label = str(val) + u'\N{DEGREE SIGN}'
        if fahrenheit:
            label += "F"
        else:
            label += "C"

        return label
            
    if re.search(r'^(h|sm)', typ):
        label = str(val) + "%"
        return label

    return None


if __name__ == '__main__':
    poll = Setting.query.filter(Setting.name == 'polling interval minutes').first()
    if not poll:
        logger.error("could not determine polling interval from db")
        sys.stderr.write("error\n")
        sys.exit(1)

    if now.minute % poll.value > 0:
        # not the right time to be running this. exit
        sys.exit(0)
    
    fahrenheit = bool(Setting.query.filter(Setting.name == 'store temperature fahrenheit').first().value)

    main()

