from app import db
import json

class Outlet(db.Model):
    __tablename__ = 'outlets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, server_default='', unique=True)
    channel = db.Column(db.Integer, nullable=False, server_default='1', unique=True)
    state = db.Column(db.Boolean(), nullable=False, server_default='0')

    def __init__(self, name, channel):
        self.name = name
        self.channel = channel
        
    def __repr__(self):
        return json.dumps(self.simplified())

    def simplified(self):
        return {'id': self.id, 
                'name': self.name, 
                'channel': self.channel, 
                'state': self.state}
