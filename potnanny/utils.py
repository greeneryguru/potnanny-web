import os
import string
import random
import re
import time
import datetime
import requests
import hashlib
import json
from potnanny.apps.settings.models import Setting

requests.packages.urllib3.disable_warnings()

VESYNC_URL = "https://server1.vesync.com:4007"
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Instance folder path, make it independent.
INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

# Model
STRING_LEN = 64



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


def celsius_to_f(c):
    return (9.0/5.0 * c) + 32


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




  