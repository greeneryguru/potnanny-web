from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False, server_default='', unique=True)
    password = db.Column(db.String(512), nullable=False, server_default='')
    email = db.Column(db.String(128), nullable=True)
    active = db.Column(db.Boolean(), nullable=False, server_default='1')
    authenticated = db.Column(db.Boolean(), nullable=False, server_default='0')
    
    def __init__(self, username, passwd=None):
        self.username = username
        if passwd:
            self.password = passwd
    
    def __repr__(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)



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


