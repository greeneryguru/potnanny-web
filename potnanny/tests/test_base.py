import re
import os
import unittest
from flask_testing import TestCase
from potnanny.extensions import db
from potnanny.application import configure_database
from potnanny.config import TestConfig
from potnanny.application import create_app


class BaseTestCase(TestCase):
 
    def create_app(self):
        self.app = create_app(config=TestConfig)
        return self.app
        
    def setUp(self):
        configure_database(self.app, True)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        pass


