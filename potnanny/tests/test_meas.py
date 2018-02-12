from test_base import BaseTestCase
from potnanny.extensions import db
from potnanny.apps.measurement.models import Measurement
from potnanny.apps.sensor.models import Sensor
import datetime
        
            
class MeasurementTest(BaseTestCase):
    
    def test_create_delete(self):
        # create the measurement
        m = Measurement('temperature', '11:22:33:44:55', 50)
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

        
        