from test_base import BaseTestCase
from potnanny.extensions import db
from potnanny.apps.outlet.models import Outlet
from potnanny.apps.schedule.models import Schedule
import re

class ScheduleTest(BaseTestCase):
    
    def test_create(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        
        s = Schedule(o.id, '7:00am', '7:00pm', 127, 1)
        db.session.add(s)        
        db.session.commit()
        
        self.assertTrue(s.days == 127)
        self.assertTrue(s.on_time == '7:00am')
        self.assertTrue(s.off_time == '7:00pm')
        self.assertTrue(s.run_days()[0] == 'Every Day')
        self.assertTrue(s.active)
        
        s.days = 7
        self.assertTrue(re.search(r'th', " ".join(s.run_days()), 
                                  re.IGNORECASE))
        self.assertTrue(re.search(r'fr', " ".join(s.run_days()), 
                                  re.IGNORECASE))
        self.assertTrue(re.search(r'sa', " ".join(s.run_days()), 
                                  re.IGNORECASE))
        self.assertFalse(re.search(r'we', " ".join(s.run_days()), 
                                   re.IGNORECASE))
    
    def test_delete(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        
        s = Schedule(o.id, '7:00 am', '7:00pm', 127, 1)
        db.session.add(s)        
        db.session.commit()
        
        db.session.delete(s)
        db.session.commit()
        
        # gone from session?
        self.assertFalse(s in db.session)
        
        # no longer in database?
        result = Schedule.query.filter(
            Schedule.outlet_id == o.id).first()
        self.assertTrue(result is None)
    
    def test_cascade_delete(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        id = o.id
        
        s1 = Schedule(o.id, '7:00 am', '7:00pm', 127, 1)
        s2 = Schedule(o.id, '9:00 am', '9:30am', 127, 1)
        db.session.add(s1)
        db.session.add(s2)       
        db.session.commit()
        
        db.session.delete(o)
        db.session.commit()
        
        # gone from session?
        result = Schedule.query.filter(Schedule.outlet_id == id).all()
        self.assertFalse(result)
        
    def test_edit(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        
        s = Schedule(o.id, '7:00 am', '7:00pm', 127, 1)
        db.session.add(s)        
        db.session.commit()
        
        s.days = 7
        db.session.commit()
        self.assertTrue(s.days == 7)
        
        
    def test_create_url(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        
        data = {
            'outlet_id': o.id,
            'on_time': '7:00am',
            'off_time': '7:00pm',
            'days': 7,
            'custom': 1,
        }
        response = self.client.post('/schedule/create', data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        
    def test_delete_url(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        
        s = Schedule(o.id, '7:00am', '7:00pm', 127, 1)
        db.session.add(s)        
        db.session.commit()
        
        response = self.client.post('/schedule/%d/delete' % s.id, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        
    def test_edit_url(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        
        s = Schedule(o.id, '7:00am', '7:00pm', 7, 1)
        db.session.add(s)        
        db.session.commit()
        
        data = {
            'days': 127,
        }
        response = self.client.post('/schedule/%d/edit' % s.id, data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
    