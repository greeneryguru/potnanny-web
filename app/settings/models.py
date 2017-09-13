from app import app, db

class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False, server_default='')
    value = db.Column(db.Integer, nullable=False, server_default='0')

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "%s  value %d" % (self.name, self.value)


