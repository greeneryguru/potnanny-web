from django.test import TestCase
from app.inventory.models import Sensor, Relay, PollInterval

class InventoryTests(TestCase):
    fixtures = ['inventory/inventory.json']
        
    
    """ Sensor CRUD Tests """
    def test_sensor_create(self):
        s = Sensor.objects.get_or_create(name='TEST', gpio=31)[0]
        s.save()
        self.assertEquals(s.name, 'TEST')
        
    def test_sensor_read(self):
        s = Sensor.objects.get(name='Room Temp Sensor')
        self.assertEquals(s.name, 'Room Temp Sensor')
        
    def test_sensor_update(self):
        s = Sensor.objects.get(name='Room Temp Sensor')
        s.name = 'CHANGED'
        s.save()
        self.assertEquals(s.name, 'CHANGED')
        
    def test_sensor_delete(self):
        s = Sensor.objects.get(name='Room Temp Sensor')
        s.delete()
        self.assertTrue(True)  
        
          
    """ Relay CRUD Tests """  
    def test_relay_create(self):
        s = Relay.objects.get_or_create(name='relay test')[0]
        s.save()
        self.assertEquals(s.name, 'relay test')
        
    def test_relay_read(self):
        s = Relay.objects.get(name='Fan 1 Power')
        self.assertEquals(s.name, 'Fan 1 Power')
        
    def test_relay_update(self):
        s = Relay.objects.get(name='Fan 1 Power')
        s.name = 'TEST'
        s.save()
        self.assertEquals(s.name, 'TEST')
        
    def test_relay_delete(self):
        s = Relay.objects.get(name='Fan 1 Power')
        s.delete()
        self.assertTrue(True)    
        

    """ PollInterval """  
    def test_polli_create(self):
        s = PollInterval.objects.get_or_create(value=30)[0]
        s.save()
        self.assertEquals(s.value, 30)
        
    def test_polli_read(self):
        s = PollInterval.objects.get(value=10)
        self.assertEquals(s.value, 10)
        
    def test_polli_update(self):
        s = PollInterval.objects.get(value=10)
        s.value = 30
        s.save()
        self.assertEquals(s.value, 30)
        
    def test_polli_delete(self):
        s = PollInterval.objects.get(value=10)
        s.delete()
        self.assertTrue(True)    
 
        

