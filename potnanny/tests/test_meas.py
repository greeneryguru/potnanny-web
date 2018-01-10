from test_base import BaseTestCase
from potnanny.extensions import db
from potnanny.apps.measurement.models import MeasurementType, Measurement, \
                                            MeasurementAverage
from potnanny.apps.sensor.models import Sensor
from potnanny.apps.measurement.views import sensors_reporting_in_range
import datetime


class MeasurementTypeTest(BaseTestCase):
    
    def test_create(self):
        m = MeasurementType('test')
        
        # commit inital user
        db.session.add(m)
        
        # check setting NOT auto-set before commit
        self.assertFalse(m.active)
        
        db.session.commit()
        
        # check setting get auto-set after commit
        self.assertTrue(m.active)
        
        # check user in session
        self.assertTrue(m in db.session)
        self.assertTrue(m.name == 'test')
        

    def test_delete(self):
        m = MeasurementType('test')
        db.session.add(m)
        db.session.commit()
        
        # test deleting the object
        db.session.delete(m)
        db.session.commit()
        
        # user gone from session?
        self.assertFalse(m in db.session)
        
        # matching username no longer in database
        m = MeasurementType.query.filter(
             MeasurementType.name == 'test').first()
        self.assertTrue(m is None)
        

    def test_edit(self):
        m = MeasurementType('test')
        db.session.add(m)
        db.session.commit()
        
        m.name = 'foobar'
        db.session.commit()
        self.assertTrue(m.name == 'foobar')
        
    def test_create_url(self):
        data = {
            'name': 'test',
        }
        response = self.client.post('/measurementtype/create', data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        results = MeasurementType.query.filter(
            MeasurementType.name == 'test').all()
        self.assertTrue(results)
    
    
    def test_delete_url(self):
        o = MeasurementType('foo')
        db.session.add(o)
        db.session.commit()
        id = o.id
        
        response = self.client.post('/measurementtype/%d/delete' % o.id, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        results = MeasurementType.query.get(id)
        self.assertFalse(results)
    
        
    def test_edit_url(self):
        o = MeasurementType('test')
        db.session.add(o)
        db.session.commit()
        data = {
            'id': o.id,
            'name': 'foo',
            'active': 1,
        }
        response = self.client.post('/measurementtype/%d/edit' % o.id, data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        results = MeasurementType.query.get(o.id)
        self.assertTrue(results.name == 'foo')
        
            
class MeasurementTest(BaseTestCase):
    
    def test_create_delete(self):
        # fetch a measurement type to associate our measurement to
        mt = MeasurementType.query.get(1)
        
        # create a sensor to associate the measurement to
        s = Sensor("test", 2)
        db.session.add(s)
        db.session.commit()
        
        # create the measurement
        m = Measurement(mt.id, s.id, 50, '50%')
        db.session.add(m)
        db.session.commit()
        
        # check value
        self.assertTrue(m.value == 50)
        
        # date/time auto populated?
        self.assertTrue(m.date_time is not None)
        
        # delete the object
        db.session.delete(m)
        db.session.commit()
              
        # gone from session?
        self.assertFalse(m in db.session)

             
    def test_cascade_delete(self):
        # fetch a measurement type to associate our measurements to
        mt = MeasurementType.query.get(1)
        self.assertFalse(mt is None)
        
        # create a sensor to associate the measurements to
        s = Sensor("test", 2)
        db.session.add(s)
        db.session.commit()
        
        # create some measurements
        for n in (10,20,30,40,50):
            m = Measurement(mt.id, s.id, n, '%d%%' % n)
            db.session.add(m)
        
        db.session.commit()
        
        # delete the MeasurementType
        db.session.delete(mt)
        db.session.commit()
        self.assertFalse(mt in db.session)
        
        # associated measurement(s) gone too?
        items = Measurement.query.filter(Measurement.type_id == 1).all()
        self.assertFalse(items)
             
    def test_latest(self):
        mt = MeasurementType.query.get(1)
        self.assertFalse(mt is None)
        
        # create a sensor to associate the measurements to
        s = Sensor("test", 2)
        db.session.add(s)
        db.session.commit()
        
        m = Measurement(mt.id, s.id, 50, '50%')
        db.session.add(m)
        db.session.commit()
        
        result = self.client.get('/measurement/type/%d/latest' % mt.id,
                                 follow_redirects=True)
        self.assertTrue('"value": 50.0' in str(result.data))
        
        result = self.client.get('/measurement/type/%d/sensor/%d/latest' % 
                                 (mt.id, s.id), follow_redirects=True)
        self.assertTrue('"value": 50.0' in str(result.data))
        
     
class MeasurementAvgTest(BaseTestCase):
    
    def test_create_delete(self):
        mt = MeasurementType.query.get(1)
        self.assertFalse(mt is None)
        
        # create a sensor to associate the measurements to
        s = Sensor("test", 2)
        db.session.add(s)
        db.session.commit()
        
        m = MeasurementAverage(mt.id, s.id, 50, 40, 60)
        db.session.add(m)
        db.session.commit()
        
        # check values
        self.assertTrue(m.avg == 50)
        self.assertTrue(m.min == 40)
        self.assertTrue(m.max == 60)
        
        # query and check results
        items = MeasurementAverage.query.filter(
            MeasurementAverage.sensor_id == s.id).all()
        self.assertTrue(len(items) == 1)   
        
        # delete the object
        db.session.delete(m)
        db.session.commit()
              
        # gone from session?
        self.assertFalse(m in db.session)
        
        
    def test_cascade_delete(self):    
        mt = MeasurementType.query.get(1)
        self.assertFalse(mt is None)
        
        # create a sensor to associate the measurements to
        s = Sensor("test", 2)
        db.session.add(s)
        db.session.commit()
        sid = s.id
        
        # create some measurement averages
        for n in ((40,32,45), (41,30,46), (50,40,60)):
            navg, nmin, nmax = n
            m = MeasurementAverage(mt.id, s.id, navg, nmin, nmax)
            db.session.add(m)
    
        db.session.commit()
        
        # query and check results in database
        items = MeasurementAverage.query.filter(
            MeasurementAverage.sensor_id == sid).all()
        self.assertTrue(len(items) == 3)   
            
        # delete the sensor
        db.session.delete(s)
        db.session.commit()
        self.assertFalse(s in db.session)
        
        # associated measurement(s) gone too?
        items = MeasurementAverage.query.filter(
            MeasurementAverage.sensor_id == sid).all()
        self.assertFalse(items)
             
             
class HelperTest(BaseTestCase):
    
    def test_sensors_reporting(self):
        # fetch a measurement type to associate our measurement to
        mt = MeasurementType.query.get(1)
        
        # create a sensor to associate the measurement to
        s = Sensor("test", 2)
        db.session.add(s)
        db.session.commit()
        
        # create the measurement and reporting timeframe
        m = Measurement(mt.id, s.id, 50, '50%')
        db.session.add(m)
        db.session.commit()
        
        # test that sensor is included in results
        now = datetime.datetime.now()
        then = now - datetime.timedelta(minutes=1)
        results = sensors_reporting_in_range(mt.id, then, now)
        self.assertTrue(results)
        self.assertTrue(s in results)
        
        # different time window should produce zero results
        now = now - datetime.timedelta(minutes=10)
        then = now - datetime.timedelta(minutes=1)
        results = sensors_reporting_in_range(mt.id, then, now)
        self.assertFalse(results)
        self.assertTrue(s not in results)
          
    
        
    
        
        