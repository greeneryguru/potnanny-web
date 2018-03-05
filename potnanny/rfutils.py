import os
import re
import errno
import subprocess

class TXChannelControl(object):

    def __init__(self, **kwargs):
        self.send_command = '/var/www/potnanny/potnanny/scripts/send'
        self.base_code = 36000
        self.pulse_width = 170
        self.gpio_pin = 11
        self.sudo = False
        self.type = 'Intey'

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
    """
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
    get a rf code for turning a channel on or off

    params:
        - outlet type (Intey, Etekcity, Other...)
        - channel number (int)
        - state number (int)(1 = on, 0 = off)
    returns:
        a str representation of a number
    """
    def tx_code(self, typ, channel, state):
        code = self.base_code
        code += (channel << 1)
        
        """
        on/off code schemes are different for these brands.
        
        Etekcity = last 4 bytes [ OFF (1100) / ON (0011) ]
        Intey = last 1 byte [ OFF (0) / ON (1) ]
        
        I believe the Etekcity method is considered the more normal method, so
        we treat this one as the default.
        
        """
        if re.search(r'Intey', typ, re.IGNORECASE):
            code += state

        else:
            if state == 0:
                code += 12
            else:
                code += 3
    
        return str(code)  


    
