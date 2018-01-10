from test_base import BaseTestCase
from potnanny.extensions import db
from potnanny.apps.outlet.models import Outlet


class OutletTest(BaseTestCase):
    
    def test_create(self):
        o = Outlet('test', 42)
        db.session.add(o)
        
        # check setting NOT auto-set before commit
        self.assertFalse(o.active)
        
        db.session.commit()
        
        # check setting get auto-set after commit
        self.assertTrue(o.active)
        
        # check user in session
        self.assertTrue(o in db.session)

        self.assertTrue(o.name == 'test')
        self.assertTrue(o.channel == 42)
        
    
    def test_delete(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        
        # test deleting the object
        db.session.delete(o)
        db.session.commit()
        
        # user gone from session?
        self.assertFalse(o in db.session)
        
        # matching username no longer in database
        o = Outlet.query.filter(Outlet.name == 'test').first()
        self.assertTrue(o is None)
        

    def test_edit(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        
        o.name = "foo"
        db.session.commit()
        self.assertTrue(o.name == 'foo')
        
        
    def test_create_url(self):
        data = {
            'name': 'test',
            'channel': 42,
        }
        response = self.client.post('/outlet/create', data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        
    def test_delete_url(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        
        response = self.client.post('/outlet/%d/delete' % o.id, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        
    def test_edit_url(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        data = {
            'name': 'foo',
        }
        response = self.client.post('/outlet/%d/edit' % o.id, data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        
    def test_toggle_state(self):
        o = Outlet('test', 42)
        db.session.add(o)
        db.session.commit()
        
        response = self.client.post('/outlet/%d/toggle' % o.id,
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('"state": false' in str(response.data))
    