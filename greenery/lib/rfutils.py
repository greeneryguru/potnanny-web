import re
import serial
from greenery.apps.admin.models import Setting
from greenery.lib.ttycmd import cmd_codes


"""
send a code to the serial tty.
results should be either 'ok' or 'fail'

returns 0 on success. 
"""
def tx433(chan, state):
    failure = 1
    base = Setting.query.filter(Setting.name == 'rf tx base code').first().value
    if not base:
        raise
    
    code = int(self.base_code)
    code += (chan << 1)
    code += state

    try:
        ser = serial.Serial(sdevice, 9600, 5)
        time.sleep(3)
        if not ser.isOpen:
            ser.open(sdevice)
        
        ser.flushInput()
    except Exception as x:
        logger.error(x)
        return 1

    cmd = "%d%d\n" % (cmd_codes['tx'], code)
    ser.write(cmd.encode('UTF-8'))
    line = ser.readline().decode().strip()
    if re.search(r'^ok', line, re.IGNORECASE):
        failure = 0

    ser.close()
    return failure


