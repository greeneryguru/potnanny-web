from app import db
from app.outlet.models import Outlet
from app.lib.greenery.utils import WeekdayMap
import json


class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    outlet_id = db.Column(db.Integer, db.ForeignKey('outlets.id'))
    on_time = db.Column(db.String(16), nullable=False, server_default='')
    off_time = db.Column(db.String(16), nullable=False, server_default='')
    days = db.Column(db.Integer, nullable=False, server_default='127')
    
    outlet = db.relationship('Outlet',
                           backref=db.backref('schedules', cascade="all, delete-orphan"), lazy='joined')


    def __repr__(self):
        o = Outlet.query.filter(Outlet.id == self.outlet_id).first()
        d = ",".join(self.run_days())
        return "%s %s/%s (%s)" % (o.name, self.on_time,
                    self.off_time, d)


    def simplified(self):
        return {'id': self.id, 
                'outlet_id': self.outlet_id, 
                'on_time': self.hour,
                'off_time': self.minute,
                'days': self.outlet_state,
                }
    

    def run_days(self):
        results = [];
        dow = WeekdayMap(show_first=2).reverse_ordered_list()
        if self.days == 127:
            results.append('Every Day')
        else:
            for item in dow:
                if (self.days & item[1]):
                    results.append(item[0])

        return results


    def runs_on(self, wkday):
        for k, v in self.data:
            if re.search(wkday, v, re.IGNORECASE):
                return True

        return False

        
