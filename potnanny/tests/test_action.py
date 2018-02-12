from test_base import BaseTestCase
from potnanny.extensions import db
from potnanny.apps.action.models import Action, ActionProcess, ActionManager
from potnanny.apps.sensor.models import Sensor
from potnanny.apps.measurement.models import Measurement
import datetime
import time

class ActionTest(BaseTestCase):
    
    def test_create_delete(self):
        # create action
        a = Action('test action', 'temperature', 'outlet-12345', '11:22:33:44:55', 'switch-outlet')
        db.session.add(a)
        db.session.commit()
        
        self.assertTrue(a in db.session())
        self.assertTrue(a.active)
        
        # delete action
        db.session.delete(a)
        db.session.commit()
        
        self.assertFalse(a in db.session())
    
    def test_edit(self):
        # create action
        a = Action('test action', 'temperature', 'outlet-12345', '11:22:33:44:55', 'switch-outlet')
        db.session.add(a)
        db.session.commit()
        
        a.action_type = 'sms-message'
        a.sms_recipient = '+18005551212'
        db.session.commit()
        
        self.assertTrue(a.action_type == 'sms-message')
        self.assertTrue(a.sms_recipient == '+18005551212')
           
    def test_create_url(self):
        data = {
            'name': 'test',
            'measurement_type': 'temperature',
            'outlet_id': 'outlet-12345',
            'action_type': 'sms-message',
            'sms-recipient': '+18005551212',
            'on_condition': 'GT',
            'on_threshold': 80,
            'wait_minutes': 5,
        }
        response = self.client.post('/action/create', data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        
    def test_delete_url(self):
        a = Action('test action', 'temperature', 'outlet-12345', '11:22:33:44:55', 'switch-outlet')       
        db.session.add(a)
        db.session.commit()
        id = a.id
        
        self.assertTrue(a in db.session())
        response = self.client.post('/action/%d/delete' % a.id, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        results = Action.query.get(id)
        self.assertFalse(results) 
        
        
class ActionManagerTest(BaseTestCase):
    
    def test_init(self):
        mgr = ActionManager()
        
    def test_eval_conditionals(self):
        mgr = ActionManager() 
        self.assertTrue(mgr.meets_condition(90,'gt',80))
        self.assertTrue(mgr.meets_condition(78,'lt',80))
        self.assertTrue(mgr.meets_condition(2,'eq',2))
    
    def test_triggers(self):
        m1 = Measurement('11:22:33:44:55', 'temperature', 22)
        m2 = Measurement('11:22:33:44:55', 'temperature', 18)
        
        a = Action('test action', 'temperature', 'bogus-outlet-id', '11:22:33:44:55', 'switch-outlet')
        a.on_condition = 'GT'
        a.on_threshold = 21
        a.off_condition = 'LT'
        a.off_threshold = 19
        a.sensor_address = '11:22:33:44:55'
        
        db.session.add(a)
        db.session.add(m1)
        db.session.add(m2)
        db.session.commit()
        
        mgr = ActionManager()
        trigger = mgr.measurement_tripped(a, m1)
        self.assertTrue(trigger == 'on')
        
        trigger = mgr.measurement_tripped(a, m2)
        self.assertTrue(trigger == 'off')
        
    def test_start_processes(self):
        m1 = Measurement('11:22:33:44:55', 'temperature', 22)
        
        a = Action('test action', 'temperature', 'bogus-outlet-id', '11:22:33:44:55', 'switch-outlet')
        a.on_condition = 'GT'
        a.on_threshold = 21
        a.off_condition = 'LT'
        a.off_threshold = 19
        a.sensor_address = 'any'
        a.wait_minutes = 0
        
        db.session.add(a)
        db.session.add(m1)
        db.session.commit()
        
        mgr = ActionManager()
        mgr.eval_measurement(m1)
        
        p = ActionProcess.query.get(1)
        self.assertTrue(p)
        self.assertTrue(p.active is True)
        
    def test_end_processes(self):
        now = datetime.datetime.now()
        then = now - datetime.timedelta(minutes=2)
        
        m1 = Measurement('11:22:33:44:55', 'temperature', 23, then)
        m2 = Measurement('11:22:33:44:55', 'temperature', 18, now)
        
        a = Action('test action', 'temperature', 'bogus-outlet-id', '11:22:33:44:55', 'switch-outlet')
        a.on_condition = 'GT'
        a.on_threshold = 21
        a.off_condition = 'LT'
        a.off_threshold = 19
        a.sensor_address = 'any'
        a.wait_minutes = 0
        
        db.session.add(m1)
        db.session.add(m2)
        db.session.add(a)
        db.session.commit()
        
        mgr = ActionManager()
        mgr.eval_measurement(m1)
        mgr.eval_measurement(m2)
        
        # confirm that process is locked, but still active
        p = ActionProcess.query.get(1)
        self.assertTrue(p)
        self.assertTrue(p.active is True)
        
        # another measurement should shut down previous process, and
        # create a new one
        mgr.eval_measurement(m2)
        p = ActionProcess.query.get(1)
        self.assertTrue(p)
        self.assertTrue(p.active is False)
        
        p = ActionProcess.query.all()
        self.assertTrue(len(p) == 2)
        
        
        
        