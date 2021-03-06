from test_base import BaseTestCase
from potnanny.extensions import db
from potnanny.apps.sensor.models import Sensor


class SensorTest(BaseTestCase):
    
    def test_create(self):
        s = Sensor('test', '11:22:33:44:55')
        
        # commit inital user
        db.session.add(s)
        db.session.commit()
        
        # check user in session
        self.assertTrue(s in db.session)

        self.assertTrue(s.name == 'test')
        self.assertTrue(s.address == '11:22:33:44:55')
        
    def test_delete(self):
        s = Sensor('test', '11:22:33:44:55')
        db.session.add(s)
        db.session.commit()
        
        # test deleting the object
        db.session.delete(s)
        db.session.commit()
        
        # user gone from session?
        self.assertFalse(s in db.session)
        
        # matching username no longer in database
        s = Sensor.query.filter(Sensor.name == 'test').first()
        self.assertTrue(s is None)
        

    def test_edit(self):
        s = Sensor('test', '11:22:33:44:55')
        db.session.add(s)
        db.session.commit()
        
        s.name = 'foo'
        db.session.commit()
        self.assertTrue(s.name == 'foo')
        
        
    def test_create_url(self):
        data = {
            'name': 'test',
            'address': '11:22:33:44:55',
        }
        response = self.client.post('/sensor/create', data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        
    def test_delete_url(self):
        s = Sensor('test', '11:22:33:44:55')
        db.session.add(s)
        db.session.commit()
        
        response = self.client.post('/sensor/%d/delete' % s.id, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        

    """        
    def test_edit_url(self):
        s = Sensor('test', '11:22:33:44:55')
        db.session.add(s)
        db.session.commit()
        data = {
            'name': 'foo',
            'address': '11:22:33:44:66'
        }
        response = self.client.post('/sensor/%d/edit' % s.id, data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
    """    
        
    