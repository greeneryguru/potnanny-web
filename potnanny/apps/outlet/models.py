from potnanny.extensions import db
from potnanny.rfutils import TXChannelControl
import json


class Outlet(db.Model):
    __tablename__ = 'outlets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, server_default='', unique=True)
    on_code = db.Column(db.Integer, nullable=False, unique=True)
    off_code = db.Column(db.Integer, nullable=False, unique=True)
    state = db.Column(db.Boolean(), nullable=False, server_default='0')
    active = db.Column(db.Boolean(), nullable=False, server_default='1')

    def __init__(self, name, on, off):
        self.name = name
        self.on_code = on
        self.off_code = off
        
    def __repr__(self):
        return json.dumps(self.as_dict())

    def as_dict(self):
        return {'id': self.id, 
                'name': self.name,
                'on_code': self.on_code,
                'off_code': self.off_code,
                'state': self.state, 
                'active': self.active }
    
    
    """
    transmit rf code to turn the outlet 'on'
    
    params:
        - status: return json status of outlet after command.
    returns:
        zero on success. non-zero on failure. 
        Unless 'status' option is set, then the return will be JSON status 
        of the Outlet.
    
    -- OLD CODE --
    def on(self, status=False):
        rval = self.set_state(1)
        if status:
            return str(self)
        else:
            return rval

    """ 
    def on(self, status=False):
        tx = TXChannelControl(sudo=True)
        rval, msg = tx.send_code(self.on_code)
        if not rval:
            self.state = 1
            db.session.commit()
        else:
            print("%d, %s" % (rval,  msg))
    
    """
    same as 'on', but turns outlet 'off'
    
    -- OLD CODE --
    def off(self, status=False):
        rval = self.set_state(0)
        if status:
            return str(self)
        else:
            return rval
    
    """
    def off(self, status=False):
        tx = TXChannelControl(sudo=True)
        rval, msg = tx.send_code(self.off_code)
        if not rval:
            self.state = 0
            db.session.commit()
        else:
            print("%d, %s" % (rval,  msg))
    
    
    """
    send rf code to set an outlet on or off
    
    params:
        state 0|1
    returns:
        zero on success, non-zero on fail

    def set_state(self, state):
        tx = TXChannelControl(sudo=True)
        rval, msg = tx.send_control(self.channel, state)
        if not rval:
            self.state = state
            db.session.commit()
        
        return rval
    """
