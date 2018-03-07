import os
import re
import errno
import subprocess

class TXChannelControl(object):

    def __init__(self, **kwargs):
        self.command = '/var/www/potnanny/potnanny/scripts/codesend'
        self.base_code = 36000
        self.pulse_width = 193
        self.protocol = 1
        self.gpio_pin = 11
        self.sudo = False

        for k, v in kwargs.items():
            setattr(self, k, v)
    
        # if not os.path.exists(self.send_command):
        #    raise IOError(errno.ENOENT, 'File not found', self.send_command)

   
    """
    send an on/off state command to a channel

    params:
        - channel number (int)
        - state number (int)(1 = on, 0 = off)
    returns:
        a tuple (exit-code, message)
        exit-code = 0 on success, non-zero on failure

    def send_control(self, channel, state):
        cmd = []
        if self.sudo:
            cmd.append('sudo')

        cmd.append(self.send_command)
        cmd.append(self.tx_code(self.type, channel, state))
        try:
            child = subprocess.Popen(cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE )
            output, errors = child.communicate()
            if child.returncode:
                return (child.returncode, errors)
            else:
                return (child.returncode, output)
        except:
            return (255, 'unexpected command failure')

    """
    
          
    """
    send a tx code to a channel

    params:
        - a code number (int)
    returns:
        a tuple (exit-code, message)
        exit-code = 0 on success, non-zero on failure
    """
    def send_code(self, code):
        cmd = []
        if self.sudo:
            cmd.append('sudo')

        cmd.append(self.command)
        cmd.append(str(code))
        cmd.append(str(self.protocol))
        cmd.append(str(self.pulse_width))
        
        # print("tx command: %s" % cmd)
        
        try:
            child = subprocess.Popen(cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE )
            output, errors = child.communicate()
            if child.returncode:
                return (child.returncode, errors)
            else:
                return (child.returncode, output)
        except Exception as x:
            # print(x)
            return (255, 'unexpected command failure')

    
    
    """
    get a rf code for turning a channel on or off

    params:
        - channel number (int)
        - state number (int)(1 = on, 0 = off)
    returns:
        a str representation of a number
    """
    def tx_code(self, channel, state):
        code = self.base_code
        code += (channel << 1)
        code += state
        
        return str(code)  


    
