from test_base import BaseTestCase
from potnanny.extensions import db
from potnanny.apps.settings.models import Setting

class SettingTest(BaseTestCase):
    
    def test_create(self):
        obj = Setting('c', 10)
        db.session.add(obj)
        db.session.commit()
        self.assertTrue(obj.temperature == 'c')
        self.assertTrue(obj.interval == 10)
        
    def test_delete(self):
        obj = Setting('f', 15)
        db.session.add(obj)
        db.session.commit()
        
        db.session.delete(obj)
        db.session.commit()
        
        # gone from session?
        self.assertFalse(obj in db.session)
        
        # no longer in database?
        result = list(Setting.query.filter(
            Setting.temperature == 'f',
            Setting.interval == 15))
        self.assertFalse(result)
        
    def test_edit(self):
        obj = Setting('f', 15)
        db.session.add(obj)
        db.session.commit()
        
        obj.interval = 100
        db.session.commit()
        
        result = list(Setting.query.filter(
            Setting.temperature == 'f',
            Setting.interval == 100))
        self.assertTrue(result)
        
    def test_edit_url(self):
        obj = Setting('f', 2)
        db.session.add(obj)
        db.session.commit()
        
        data = {
            'id': obj.id,
            'temperature': 'c',
            'interval': 10
        }
        response = self.client.post('/settings/%d' % obj.id, data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
    