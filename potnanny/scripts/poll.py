#!/usr/bin/env python3


"""

Poll sensors to get temp/humid/soil-moisture etc...

The Arduino accepts number-based command codes over the usb serial connection.
Commands can have a variable number of characters, depending on the cmd-type,
measurement-type, sensor or pin type.
Code-mappings are found in potnanny/lib/ttycmd.py {TTY_CODES}

Examples,
    
    "0012\n"    =   0=mode(get),
                    0=measurement(temperature),
                    1=sensor(dht22),
                    2=pin(2)

    "02014\n"   =   0=mode(get),
                    2=measurement(soil-moisture),
                    0=type(analog),
                    14=pin(14)

Commands MUST be terminated with '\n'!

"""

import os
import sys
import re
import time
import datetime
import serial
sys.path.append( os.environ.get('FLASK_APP','/var/www/potnanny') )
from potnanny.application import create_app
from potnanny.extensions import db
from potnanny.apps.measurement.models import MeasurementType, Measurement
from potnanny.apps.settings.models import Setting
from potnanny.apps.sensor.models import Sensor
from potnanny.utils import TTY_CODES, SERIAL_PORT


# global vars
poll = None
fahrenheit = None
now = datetime.datetime.now().replace(second=0, microsecond=0)


def main():
    ser = None
    try:
        ser = serial.Serial(SERIAL_PORT, 9600, 5)
        time.sleep(2)
        if not ser.isOpen:
            ser.open(SERIAL_PORT)
        
        ser.flushInput()
    except Exception as x:
        sys.stderr.write("serial port failure\n")
        sys.exit(1)
    
    mtypes = MeasurementType.query.filter(
        MeasurementType.active == True).all()
    
    sensors = Sensor.query.filter(
        Sensor.active == True).all()
        
    for s in sensors:
        for typ in ('temperature', 'humidity', 'soil'):
            if re.search(typ, s.tags):
                
                # build our command sequence based on types
                cmd = build_sensor_command(s, typ)
                if not cmd:
                    # logger.warning("sensor '%s' measurement '%s' command-build failed" % (s.name, typ))
                    sys.stderr.write("sensor '%s' measurement '%s' command-build failed\n" % (s.name, typ))
                    continue

                # send code to serial tty and hope for the best ;)
                ser.write(cmd.encode('UTF-8'))

                while True:
                    # returns like; 
                    #   line = "sm,14,22" (code, address, value)
                    line = ser.readline().decode().strip()

                    if re.search(r'^ok', line, re.IGNORECASE):
                        # nothing more to read!
                        break
                    if re.search(r'^fail', line, re.IGNORECASE):
                        # logger.warning("sensor '%s' fail result '%s'" % (s.name, line))
                        sys.stderr.write("sensor '%s' fail result '%s'\n" % (s.name, line))
                        break
                    
                    atoms =  line.split(",")
                    if len(atoms) != 3:
                        # logger.warning("sensor '%s' garbled output '%s" % (s.name, line))
                        sys.stderr.write("sensor '%s' garbled output '%s'\n" % (s.name, line))
                        continue

                    code,addr,val = atoms
                    val = float(val)
                    if code == 't' and fahrenheit:
                        val = val * 1.8 + 32

                    success = False
                    for mt in mtypes:
                        if mt.code() == code:
                            success = True
                            label = format_label(code, val, fahrenheit)
                            m = Measurement(
                                    mt.id, 
                                    s.id, 
                                    "%0.1f" % float(val), 
                                    label, 
                                    now
                            )
                            db.session.add(m)

                    if not success:
                        # logger.warning("could not match MeasurementType object to tag like '%s'" % code)
                        sys.stderr.write("could not match MeasurementType object to tag like '%s'\n" % code)
                        continue
                    
        db.session.commit()
    ser.close()


def build_sensor_command(sensor, typ):
    cmd = "%d%d" % (TTY_CODES['get'], TTY_CODES[typ])

    if re.search(r'temp', typ):
        devices = ('dht11','dht22')
        for d in devices:
            if re.search(d, sensor.tags):
                cmd += "%d%d\n" % (TTY_CODES[d], sensor.address)

    elif re.search(r'soil', typ):
        devices = ('analog','digital')
        for d in devices:
            if re.search(d, sensor.tags):
                cmd += "%d%d\n" % (TTY_CODES[d], sensor.address)
    
    if cmd[-1] == '\n':
        return cmd
    else:
        sys.stderr.write("incomplete poll tty command '%'\n" % cmd)
        # logger.warning("incomplete poll tty command '%'" % cmd)

    return None


def format_label(typ, val, fahrenheit=False):
    if re.search(r'^t', typ):
        label = "%0.1f" % val + u'\N{DEGREE SIGN}'
        if fahrenheit:
            label += "F"
        else:
            label += "C"

        return label
            
    if re.search(r'^(h|sm)', typ):
        label = "%0.1f" % val + "%"
        return label

    return None


if __name__ == '__main__':
    
    app = create_app()
    app.app_context().push()
    
    poll = Setting.query.filter(
        Setting.name == 'polling interval minutes'
    ).first()

    if not poll:
        # logger.error("could not determine polling interval from db")
        sys.stderr.write("error. could not determine polling interval from db\n")
        sys.exit(1)

    if now.minute % poll.value > 0:
        # not the right time to be running this. exit
        sys.exit(0)
    
    fahrenheit = bool(
        Setting.query.filter(
            Setting.name == 'store temperature fahrenheit'
        ).first().value
    )

    main()


