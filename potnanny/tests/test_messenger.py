from test_base import BaseTestCase
from potnanny.extensions import db
from potnanny.apps.messenger.models import TwilioAccount

class TwilioTest(BaseTestCase):
    
    def test_create(self):
        obj = TwilioAccount('foo', 'bar', '+15551212')
        db.session.add(obj)
        db.session.commit()
        self.assertTrue(obj.sid == 'foo')
        self.assertTrue(obj.token == 'bar')
        self.assertTrue(obj.number == '+15551212')
        
    def test_delete(self):
        obj = TwilioAccount('foo', 'bar', '+15551212')
        db.session.add(obj)
        db.session.commit()
        
        db.session.delete(obj)
        db.session.commit()
        
        # gone from session?
        self.assertFalse(obj in db.session)
        
        # no longer in database?
        result = TwilioAccount.query.filter(
            TwilioAccount.sid == 'foo' and
            TwilioAccount.token == 'bar').first()
        self.assertTrue(result is None)
        
    def test_edit(self):
        obj = TwilioAccount('foo', 'bar', '+15551212')
        db.session.add(obj)
        db.session.commit()
        
        obj.token = 'baz'
        db.session.commit()
        
        result = TwilioAccount.query.filter(
            TwilioAccount.sid == 'foo').first()
        self.assertTrue(result.token == 'baz')
        
    def test_create_url(self):        
        data = {
            'sid': 'foo',
            'token': 'bar',
            'number': '+15551212'
        }
        response = self.client.post('/messenger/account/create', data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
    
    def test_delete_url(self):        
        obj = TwilioAccount('foo', 'bar', '+15551212')
        db.session.add(obj)
        db.session.commit()
        
        response = self.client.post('/messenger/account/%d/delete' % obj.id, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
    
    def test_edit_url(self):      
        obj = TwilioAccount('foo', 'bar', '+15551212')
        db.session.add(obj)
        db.session.commit()
        
        data = {
            'id': obj.id,
            'sid': 'test',
            'token': 'test',
            'number': '+15558000'
        }
        
        response = self.client.post('/messenger/account/%d/edit' % obj.id,
                                    data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        result = TwilioAccount.query.get(1)
        self.assertTrue(result)
        self.assertTrue(result.token == 'test')
        
        
        