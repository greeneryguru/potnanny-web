import os
import string
import random
import re
import time
import datetime
import serial


BASEDIR = os.path.abspath(os.path.dirname(__file__))

SERIAL_PORT = '/dev/ttyUSB0'

# Instance folder path, make it independent.
INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

# Model
STRING_LEN = 64

TTY_CODES = {
    'get':          0,
    'set':          1,
    'tx':           2,

    'temperature':  0,
    'humidity':     1,
    'soil':         2,

    'analog':       0,
    'digital':      1,

    'dht11':        0,
    'dht22':        1,
}


def get_current_time():
    return datetime.datetime.utcnow()


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception as e:
        raise e


"""
send a code to the serial tty.
response back should be either 'ok' or 'fail'

returns 0 on success. 
"""
def rf_transmit(chan, state):
    failure = 1
    base = None
    pin = None

    try:
        pin = Setting.query.filter(
            Setting.name == 'rf tx pin').first().value
        base = Setting.query.filter(
            Setting.name == 'rf tx base code').first().value
        brand = Setting.query.filter(
            Setting.name == 'rf outlet brand').first().value
    except:
        return 1

    # build our code using the base starting number, and bit-shifting in
    # channel and on/off state info.
    code = int(base)
    code += (chan << 1)
    if brand == 1:
        code += state
    if brand == 2:
        # Etekcity outlets
        if not state:
            code += 9
        
    try:
        ser = serial.Serial(SERIAL_PORT, 9600, 5)
        time.sleep(2)
        if not ser.isOpen:
            ser.open(SERIAL_PORT)
        
        ser.flushInput()
    except Exception as x:
        return 1

    cmd = "%d%02d%d\n" % (TTY_CODES['tx'], pin, code)
    ser.write(cmd.encode('UTF-8'))
    line = ser.readline().decode().strip()
    if re.search(r'^ok', line, re.IGNORECASE):
        failure = 0

    ser.close()
    return failure



class WeekdayMap(object):
    """
    Map days of the week to numbers.
    Used to store day-of-week schedules in a single number.

    Usage:
        dw = WeekdayMap()
        print dw.ordered_list()
        print dw.reverse_ordered_list()
        print dw.get_dict()

    Abbreviation. 
      To truncate the day of week to first 2 or 3 letters, set the 'show_first' 
      option to the number of letters.

        dw = WeekdayMap(show_first=2)

        If you want the un-modified day tags, access the dict at WeekdayMap.data

    """
    def __init__(self, **kwargs):
        self.data = {
            64:     'Sunday',
            32:     'Monday',
            16:     'Tuesday',
            8:      'Wednesday',
            4:      'Thursday',
            2:      'Friday',
            1:      'Saturday',
        }
        self.show_first = None

        for k, v in kwargs.items():
            setattr(self, k, v)


    """
    get the mapping dict. if  show_first was set at creation, the weekdays
    will be abbreviated,

    params:
        none

    returns:
        a dict
    """
    def get_dict(self):
        d = {}
        for val, name in self.data.items():
            if self.show_first:
                name = ''.join( list(name)[0:self.show_first] )

            d.update({val: name})
                
        return d


    """
    get list with mapping of weekdays to values

    params:
        boolean (true = reverse sorting, false[default] = regular sort)

    returns:
        a list or tuples, containing [(abbreviation, number), ]  
    """
    def ordered_list(self, reverse=False):
        l = []
        d = self.get_dict()
        for k in sorted(d.keys(), reverse=reverse):
            l.append((d[k], k))
        
        return l


    """
    same as ordered_list(), but returns in reverse oder
    """
    def reverse_ordered_list(self):
        return self.ordered_list(True) 
        

    def day_value(self, wkday):
        for k, v in self.data:
            if re.search(wkday, v, re.IGNORECASE):
                return k
        
        return None



  