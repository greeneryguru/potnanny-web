from app import db
import json

(min=None, max=None, message=None)

class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    outlet_id = db.Column(db.Integer, db.ForeignKey('outlets.id'))
    hour = db.Column(db.Integer, nullable=False, server_default='0')
    minute = db.Column(db.Integer, nullable=False, server_default='0')
    outlet_state = db.Column(db.Boolean(), nullable=False, server_default='0')
    
    # is_active turns a schedule on or off
    is_active = db.Column(db.Boolean(), nullable=False, server_default='1')
    
    def __repr__(self):
        return json.dumps(self.simplified())

    def simplified(self):
        return {'id': self.id, 
                'outlet_id': self.outlet_id, 
                'hour': self.hour,
                'minute': self.minute,
                'outlet_state': self.outlet_state,
                'is_active', self.is_active,
                }
    