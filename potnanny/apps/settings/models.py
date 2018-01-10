from potnanny.extensions import db

class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48), nullable=False, server_default='')
    value = db.Column(db.Integer, nullable=False, server_default='0')
    notes = db.Column(db.String(256), nullable=True)

    def __init__(self, name, value, notes=None):
        self.name = name
        self.value = value
        if notes:
            self.notes = notes

    def __repr__(self):
        return "%s  value %d" % (self.name, self.value)

