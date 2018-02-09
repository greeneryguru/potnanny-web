from potnanny.extensions import db

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


