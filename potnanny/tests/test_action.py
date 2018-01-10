from test_base import BaseTestCase
from potnanny.extensions import db
from potnanny.apps.action.models import Action, ActionProcess, ActionManager
from potnanny.apps.outlet.models import Outlet
from potnanny.apps.sensor.models import Sensor
from potnanny.apps.measurement.models import Measurement, MeasurementType
import datetime
import time

class ActionTest(BaseTestCase):
    
    def test_create_delete(self):
        mt = MeasurementType('foo')
        o = Outlet('bar', 12)
        db.session.add(mt)
        db.session.add(o)
        db.session.commit()
        
        # create action
        a = Action('test action', mt.id, o.id, 'switch-outlet')
        db.session.add(a)
        db.session.commit()
        
        self.assertTrue(a in db.session())
        self.assertTrue(a.active)
        
        # delete action
        db.session.delete(a)
        db.session.commit()
        
        self.assertFalse(a in db.session())
        
    def test_edit(self):
        mt = MeasurementType('foo')
        o = Outlet('bar', 12)
        db.session.add(mt)
        db.session.add(o)
        db.session.commit()
        
        # create action
        a = Action('test action', mt.id, o.id, 'switch-outlet')
        db.session.add(a)
        db.session.commit()
        
        a.action_type = 'sms-message'
        a.sms_recipient = '+18005551212'
        db.session.commit()
        
        self.assertTrue(a.action_type == 'sms-message')
        self.assertTrue(a.sms_recipient == '+18005551212')
        
    def test_cascade_delete(self):
        mt = MeasurementType('foo')
        o = Outlet('bar', 12)
        db.session.add(mt)
        db.session.add(o)
        db.session.commit()
        
        # create action
        a = Action('test action', mt.id, o.id, 'switch-outlet')
        db.session.add(a)
        db.session.commit()
        
        # remove the measurement-type
        db.session.delete(mt)
        db.session.commit()
        
        self.assertFalse(a in db.session())
        
           
    def test_create_url(self):
        mt = MeasurementType('foo')
        o = Outlet('bar', 12)
        db.session.add(mt)
        db.session.add(o)
        db.session.commit()
        
        data = {
            'name': 'test',
            'measurement_id': mt.id,
            'outlet_id': o.id,
            'action_type': 'sms-message',
            'sms-recipient': '+18005551212',
            'on_condition': 'gt',
            'on_threshold': 80,
            'wait_minutes': 5,
        }
        response = self.client.post('/action/create', data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        
    def test_delete_url(self):
        mt = MeasurementType('foo')
        o = Outlet('bar', 12)
        db.session.add(mt)
        db.session.add(o)
        db.session.commit()
        
        a = Action('test action', mt.id, o.id, 'switch-outlet')       
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
    
    def test_create(self):
        mgr = ActionManager()
        self.assertTrue(mgr.meets_condition(90,'gt',80))
        self.assertTrue(mgr.meets_condition(78,'lt',80))
        self.assertTrue(mgr.meets_condition(2,'eq',2))
    
    def test_triggers(self):
        mtype = MeasurementType('foo')
        o = Outlet('bar', 12)
        s = Sensor('test sensor', 14, 'test temperature')
        
        db.session.add(mtype)
        db.session.add(o)
        db.session.add(s)
        db.session.commit()
        
        m = Measurement(mtype.id, s.id, 91, '91 degrees F')
        db.session.add(m)
        db.session.commit()
        
        # create a test action
        a = Action('test action', mtype.id, o.id, 'switch-outlet')
        a.on_condition = 'gt'
        a.on_threshold = 90
        a.off_condition = 'lt'
        a.off_threshold = 80
        a.wait_minutes = 0
        db.session.add(a)
        db.session.commit()
        
        mgr = ActionManager()
        trigger = mgr.measurement_tripped(a, m)
        self.assertTrue(trigger == 'on')
        
        m.value = 78
        m.text = '78 degrees F'
        db.session.commit()
        trigger = mgr.measurement_tripped(a, m)
        self.assertTrue(trigger == 'off')
        
        
    def test_process_states(self):
        # scaffold required objects
        mtype = MeasurementType('foo')
        o = Outlet('bar', 12)
        db.session.add(mtype)
        db.session.add(o)
        db.session.commit()
        
        # create an action
        a = Action('test action', mtype.id, o.id, 'switch-outlet')
        a.on_condition = 'gt'
        a.on_threshold = 90
        a.off_condition = 'lt'
        a.off_threshold = 80
        a.wait_minutes = 0
        db.session.add(a)
        db.session.commit()
        
        # create a dummy process for the action
        p = ActionProcess(a.id)
        p.on_datetime = datetime.datetime.now()
        p.on_trigger = '90-gt-80'
        db.session.add(p)
        db.session.commit()
        
        mgr = ActionManager()
        
        # test process for locked
        self.assertFalse(mgr.process_locked(p))
        
        p.off_datetime = datetime.datetime.now()
        p.off_trigger = '70-lt-80'
        db.session.commit()

        # test process for expired
        self.assertTrue(mgr.process_locked(p))
        self.assertTrue(mgr.process_expired(p, datetime.datetime.now()))

        
    def test_run(self):
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        then = now - datetime.timedelta(minutes=5)
        time1 = now - datetime.timedelta(minutes=2)
        time2 = now - datetime.timedelta(minutes=1)
        
        # scaffold all required objects
        mtype = MeasurementType('foo')
        o = Outlet('bar', 12)
        s = Sensor('test sensor', 14, 'test temperature')
        
        db.session.add(mtype)
        db.session.add(o)
        db.session.add(s)
        db.session.commit()
        
        m1 = Measurement(mtype.id, s.id, 91, '91 degrees F', time1)
        db.session.add(m1)
        db.session.commit()
        
        # create a test action
        a = Action('test action', mtype.id, o.id, 'switch-outlet')
        a.on_condition = 'gt'
        a.on_threshold = 90
        a.off_condition = 'lt'
        a.off_threshold = 80
        a.wait_minutes = 0
        db.session.add(a)
        db.session.commit()
        
        # action manager to test results
        mgr = ActionManager()
        self.assertTrue(mgr is not None)
        mgr.init_action(a, then, now)
          
        m2 = Measurement(mtype.id, s.id, 78, '78 degrees F', time2)
        db.session.add(m2)
        db.session.commit()
        
        mgr.init_action(a, then, now)
        proc = mgr.get_process(a)
        self.assertTrue(mgr.process_locked(proc))
        self.assertTrue(mgr.process_expired(proc))
        
        # deactivate the process
        mgr.close_process(proc)
        self.assertFalse(proc.active)
        
        