from app import db

class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, server_default='', unique=True)

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return self.name

