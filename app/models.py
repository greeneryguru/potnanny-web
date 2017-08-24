from app import db
        

class GPIOMap(db.Model):
    __tablename__ = 'gpio_maps'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, server_default='', unique=True)
    pin = db.Column(db.Integer, nullable=False, server_default='1', unique=True)
    
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        
    def __repr__(self):
        return '<GPIOMap %r pin %d>' % (self.name, self.pin)
        
    
class AppSetting(db.Model):
    __tablename__ = 'app_settings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    value = db.Column(db.Integer, nullable=False, server_default='1')
            
    def __init__(self, name=None, value=None):
        if name:
            self.setting = name
        
        if value is not None:
            self.setting = name
        
    def __repr__(self):
        return '<Setting %r>' % self.login      
            
            
            