from test_base import BaseTestCase
from potnanny.extensions import db
from potnanny.apps.settings.models import Setting

class SettingTest(BaseTestCase):
    
    def test_create(self):
        obj = Setting('test', 42, "a test setting")
        db.session.add(obj)
        db.session.commit()
        self.assertTrue(obj.value == 42)
        self.assertTrue(obj.notes == 'a test setting')
        self.assertTrue(obj.name == 'test')
        
    def test_delete(self):
        obj = Setting('test', 42, "a test setting")
        db.session.add(obj)
        db.session.commit()
        
        db.session.delete(obj)
        db.session.commit()
        
        # gone from session?
        self.assertFalse(obj in db.session)
        
        # no longer in database?
        result = Setting.query.filter(
            Setting.name == 'test').first()
        self.assertTrue(result is None)
        
    def test_edit(self):
        obj = Setting('test', 42, "a test setting")
        db.session.add(obj)
        db.session.commit()
        
        obj.value = 100
        db.session.commit()
        
        result = Setting.query.filter(
            Setting.name == 'test').first()
        self.assertTrue(result.value == 100)
        
    def test_edit_url(self):
        obj = Setting('test', 42, "a test setting")
        db.session.add(obj)
        db.session.commit()
        
        data = {
            'id': obj.id,
            'name': 'foo',
            'value': 100,
            'notes': 'bar'
        }
        response = self.client.post('/settings/%d/edit' % obj.id, data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
    