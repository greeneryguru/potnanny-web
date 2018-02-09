from potnanny.extensions import db
# from potnanny.utils import rf_transmit
import json


class Outlet(db.Model):
    __tablename__ = 'outlets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, server_default='', unique=True)
    channel = db.Column(db.Integer, nullable=False, server_default='2', unique=True)
    state = db.Column(db.Boolean(), nullable=False, server_default='0')
    active = db.Column(db.Boolean(), nullable=False, server_default='1')

    
    def __init__(self, name, channel):
        self.name = name
        self.channel = channel
        
    def __repr__(self):
        return json.dumps(self.as_dict())

    def as_dict(self):
        return {'id': self.id, 
                'name': self.name,
                'channel': self.channel,
                'state': self.state, 
                'active': self.active}
    
    
    """
    transmit rf code to turn the outlet 'on'
    
    params:
        - status: return json status of outlet after command.
    returns:
        zero on success. non-zero on failure. 
        Unless 'status' option is set, then the return will be JSON status 
        of the Outlet.
    """ 
    def on(self, status=False):
        rval = self.set_state(1)
        if status:
            return str(self)
        else:
            return rval


    """
    same as 'on', but turns outlet 'off'
    """
    def off(self, status=False):
        rval = self.set_state(0)
        if status:
            return str(self)
        else:
            return rval
    
    
    """
    send rf code to set an outlet on or off
    
    params:
        state 0|1
    returns:
        zero on success, non-zero on fail
    """
    def set_state(self, state):
        rval = rf_transmit(self.channel, state)
        if not rval:
            self.state = state
            db.session.commit()
        
        return rval

