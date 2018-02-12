from potnanny.extensions import db

class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48), nullable=False, unique=False)
    address = db.Column(db.String(24), nullable=False, unique=True)
    
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __repr__(self):
        return self.name


