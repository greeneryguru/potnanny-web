from potnanny.extensions import db


class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.String(2), nullable=False, server_default='c')
    interval = db.Column(db.Integer, nullable=False, server_default='2')

    def __init__(self, t, i):
        self.temperature = t
        self.interval = i

    def __repr__(self):
        return "temp:%s poll_interval: %d" % (self.temperature, self.interval)
