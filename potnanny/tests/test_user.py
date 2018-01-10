from test_base import BaseTestCase
from potnanny.extensions import db
from potnanny.apps.user.models import User


class UserTest(BaseTestCase):
    
    def test_create(self):
        
        # create user with minimum info
        u = User('test-user')
        self.assertTrue(u.username == 'test-user')
        
        # commit inital user
        db.session.add(u)
        
        # check setting NOT auto-set before commit
        self.assertFalse(u.active)
        
        db.session.commit()
        
        # check setting get auto-set after commit
        self.assertTrue(u.active)
        
        # check user in session
        self.assertTrue(u in db.session)

        
    def test_delete(self):
        u = User('test-user')
        
        # commit inital user
        db.session.add(u)
        db.session.commit()
        
        # test deleting the object
        db.session.delete(u)
        db.session.commit()
        
        # user gone from session?
        self.assertFalse(u in db.session)
        
        # matching username no longer in database
        u = User.query.filter(User.username == 'test-user').first()
        self.assertTrue(u is None)
        

    def test_edit(self):
        u = User('test-user', 'testpass', 'test@test.com')
        self.assertTrue(u.email == 'test@test.com')
        
        u.email = 'something@different.com'
        db.session.commit()
        self.assertTrue(u.email == 'something@different.com')
        
        
    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)
    
    
    def test_login(self):
        response = self.login(self.app.config['USERNAME'],
                              self.app.config['PASSWORD'])
        self.assertTrue("logout" in str(response.data))
    
    
    def test_logout(self):
        response = self.logout()
        self.assertTrue(response.status_code == 200)
        

    def test_create_url(self):
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'test123'
        }
        response = self.client.post('/user/create', data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        
    def test_delete_url(self):
        u = User('testuser')
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post('/user/%d/delete' % u.id, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        
    def test_edit_url(self):
        u = User('testuser')
        db.session.add(u)
        db.session.commit()
        data = {
            'email': 'test@test.com',
        }
        response = self.client.post('/user/%d/edit' % u.id, data=data, 
                                    follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        
    