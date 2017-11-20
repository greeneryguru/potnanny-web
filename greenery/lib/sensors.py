import os
import re

"""
class used to read temp information from a dallas 1-wire temp sensor, like 
the DS18B20
"""
class OneWireTemp(object):

    def __init__(self, id):
        # default path
        self.path = '/sys/bus/w1/devices'

        if os.path.exists(id):
            self.path = id
            self.id = os.path.split(id)[-1]
        elif os.path.exists(self.path + '/' + id):
            self.id = id
            self.path = self.path + '/' + id
        else:
            raise IOError('Cant find file for sensor id %s' % id)

    """
    get temperature from a sensor
    
    params: fahrenheit true/false
    returns: a dict {'type': 't = temperature', 'value': <float>, 'label': ''}
    """
    def get_temp(self, fahrenheit=False):
        temp = self.temp_from_file(self.path)
        if fahrenheit:
            return {'type': 't',
                    'value': temp * 9.0 / 5.0 + 32.0,
                    'label': 'F' }
        else:
            return {'type': 't',
                    'value': temp,
                    'label': 'C' }


    def temp_from_file(self, path):
        lines = self.read_raw(path)
        if not lines or not re.search(r'YES', lines[0]):
            time.sleep(0.4)
            lines = self.read_raw(path)
    
        match = re.search(r't=(\d+)', lines[1])
        if match:
            return float(match.group(1)) / 1000.0

        return 0.0


    def read_raw(self, path):
        fh = open(path, 'r')
        lines = fh.readlines()
        fh.close()
        return lines

