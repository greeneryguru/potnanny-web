from flask_user import UserMixin
from app import app, db 

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    confirmed_at = db.Column(db.DateTime())
    first_name = db.Column(db.Unicode(50), nullable=True, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=True, server_default=u'')
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    
    def get_id(self):
        try:
            return unicode(self.id)     # python 2
        except NameError:
            return str(self.id)         # python 3
            
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def __repr__(self):
        return '<User %r>' % self.username      
            