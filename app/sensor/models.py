from app import db
import re
import random

class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, server_default='', unique=True)
    notes = db.Column(db.String(48), nullable=True)
    profile = db.Column(db.String(64), nullable=True)

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return self.name

    def test_data(self):
        results = {}
        opts = self.profile.split(",")
        if 't' in opts:
            results['t'] = random.randint(72,78)
        
        if 'h' in opts:
            results['h'] = random.randint(55,60)

        if 'sm' in opts:
            results['sm'] = random.randint(50,58)

        return results
