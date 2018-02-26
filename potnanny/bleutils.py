from bluepy.btle import Peripheral, Characteristic, ADDR_TYPE_RANDOM, \
    AssignedNumbers


class GGDHTSensor(Peripheral):
    def __init__(self, addr):
        Peripheral.__init__(self, addr, addrType=ADDR_TYPE_RANDOM)

        self.service_uuid = "B3F72C28-2618-4E2B-9075-1B17CCA4EC66"
        self.char_uuid_map = {
            'temperature': "E60A00E9-D6A9-430F-959C-872F07E64FCE",
            'humidity': "4DF3BB88-C7CB-47B5-B213-CEA3770DB9E8",
            'co2-ppm': "6431AF8C-A5B4-47EB-BA73-B69495327E53",
        }
     
    """
    lookup uuid from name value
    
    params:
        a name string
    returns:
        a uuid string. None if name not found
    """   
    def uuid_for_name(self, key):
        for k, v in self.char_uuid_map.items():
            if k == key:
                return v
                
        return None
    
    
    """
    lookup name from uuid value
    
    params:
        a uuid string
    returns:
        a name. None if uuid not found
    """
    def name_for_uuid(self, val):
        for k, v in self.char_uuid_map.items():
            if val == v:
                return k
                
        return None
    
    
    """
    Get measurements from connected BLE device.
    
    params:
        none
    returns:
        a dict
    """
    def get_measurements(self):
        data = {}
        
        service, = [s for s in self.getServices() if s.uuid==self.service_uuid]
        if not service:
            raise
        
        uuids = self.char_uuid_map.values()
        chars = [c for c  in service.getCharacteristics() if c.uuid in uuids]
        for ch in chars:
            val = ch.read()
            name = self.name_for_uuid(ch.uuid)
            
            if name == 'temperature':
                val = int.from_bytes(val, byteorder='little', signed=True)/10
            elif name == 'humidity':
                val = int.from_bytes(val, byteorder='little', signed=False)/10
            else:
                val = int.from_bytes(val, byteorder='little', signed=False) 
            
            data[name] = val
        
        return data
        


  