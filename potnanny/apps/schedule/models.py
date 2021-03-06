from potnanny.extensions import db
from potnanny.apps.outlet.models import Outlet
from potnanny.utils import WeekdayMap
import json
import re


class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    outlet_id = db.Column(db.Integer, db.ForeignKey('outlets.id'))
    on_time = db.Column(db.String(16), nullable=False, server_default='')
    off_time = db.Column(db.String(16), nullable=False, server_default='')
    days = db.Column(db.Integer, nullable=False, server_default="127")
    custom = db.Column(db.Integer, nullable=False, server_default="0")
    active = db.Column(db.Boolean(), nullable=False, server_default='1')
    
    outlet = db.relationship("Outlet", 
                             backref=db.backref("children", 
                                                cascade="all,delete"))
    
    def __init__(self, oid, ontime, offtime, days, cust):
        self.outlet_id = oid
        self.on_time = ontime
        self.off_time = offtime
        self.days = days
        self.custom = cust

    def __repr__(self):
        d = ",".join(self.run_days())
        return "%s %s/%s (%s)" % (self.outlet.name, self.on_time,
                    self.off_time, d)

    def as_dict(self):
        return {'id': self.id, 
                'outlet': self.outlet, 
                'on_time': self.on_time,
                'off_time': self.off_time,
                'days': self.days,
                'active': self.active,
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
        dow = WeekdayMap().reverse_ordered_list()
        for d in dow:
            k, v = d
            if re.search(wkday, k, re.IGNORECASE):
                return True

        return False

        
