import re
import os
from test_base import BaseTestCase

 
class AppTests(BaseTestCase):
    
    def test_mode(self):
        self.assertTrue(self.app.config['TESTING'] == True)
         
    def test_dbexists(self):
        match = re.search(r'sqlite:///(.+)', 
                          self.app.config['SQLALCHEMY_DATABASE_URI'])
        fname = match.group(1)
        self.assertTrue(fname is not None)
        
        self.assertTrue(os.path.exists(fname))
     
    
