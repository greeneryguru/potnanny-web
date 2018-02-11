import requests
import hashlib
import json
from potnanny.extensions import db
# from flake8 import api

requests.packages.urllib3.disable_warnings()


class VesyncUser(db.Model):
    __tablename__ = 'vesync_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(48), nullable=False)
    password = db.Column(db.String(96), nullable=False)
    
    def __init__(self, name, password):
        self.username = name
        self.password = hashlib.md5(password.encode('utf-8')).hexdigest()

    def __repr__(self):
        return self.username


"""
Small convenience class to make accessing the VesyncApi a bit easier,
because this will fetch username and password for you.

All VesyncApi methods are called via self.api. Like;
    obj.api.get_devices()

If Vesync username or password are not found in database, or they are declined,
this will throw an Exception.
"""
class VesyncManager(object):
    def __init__(self, user=None, passwd=None):
        if not user or not passwd:
            u = VesyncUser.query.get(1)
            if not u:
                raise ValueError("VeSync user not defined in database")
            
            user = u.username
            passwd = u.password
             
        api = VesyncApi(user, passwd)
        if not api:
            raise InputError("Vesync username or password not accepted")
        
        self.api = api
           
 
class VesyncApi(object):
    
    """
    init and log into vesync with credentials
    """
    def __init__(self, username, password):
        self.base_url = "https://server1.vesync.com:4007"
        self.session = requests.Session()
        data = {
            'Account': username,
            'Password': password,
        }
        headers = {
            "account": username,
            "password": password,
        }
        req = requests.Request(
            'POST',
            self.base_url + "/login",
            json=data,
            headers=headers,
        )
        prepared = req.prepare()
        response = self.session.send(
            prepared, 
            verify=True
        )
        
        if response.status_code != 200 or 'error' in response.headers:
            raise RuntimeError("Invalid username or password")
        else:
            self._account = response.json()
            self._token = self._account['tk']
            self._uniqueid = self._account['id']
           
            # all future session requests should contain our token, and 
            # (maybe?) some false Agent info in the Header
            self.session.headers.update({
                'tk': self._token,
                #'User-Agent': 'Vesync/1.71.02 (iPhone; iOS 11.2.2; Scale/2.00)'
            })
            
        self._devices = []


    """
    get list of all devices associated with this account
    """
    def get_devices(self):
        req = requests.Request(
            'POST',
            self.base_url + "/loadMain",
            json=None,
            # below is a HACK headers workaround! 
            # because Session object is not sending correct headers after 
            # the first request in __init__ block.
            #
            # See: https://github.com/requests/requests/issues/4301
            #
            # Maybe I'm just doing something wrong with Session though? 
            headers=dict(self.session.headers)
        )
        prepared = req.prepare()
        response = self.session.send(
            prepared, 
            verify=True
        )
            
        self._devices = response.json()['devices']
        return self._devices


    def turn_on(self, id):
        return self.switch_outlet(id, 1)
        

    def turn_off(self, id):
        return self.switch_outlet(id, 0)
            
            
    """
    switch the outlet on or off:
    
    params:
        1. self
        2. id of the outlet/device
        3. state (0|1 (off|on))
    """
    def switch_outlet(self, oid, state):
        headers = dict(self.session.headers)
        headers.update({
            'id': self._uniqueid
        })
        data = {
            'cid': oid,
            'uri': '/relay',
            'action': 'break',
        }
        if state:
            data['action'] = 'open'
        
        req = requests.Request(
            'POST',
            self.base_url + "/devRequest",
            json=data,
            headers=headers,
        )
        prepared = self.session.prepare_request(req)
        response = self.session.send(
            prepared, 
            verify=True,
        )
        
        if response.status_code != 200 or 'error' in response.headers:
            raise RuntimeError("Relay Switch Failure")
            
        return response.json()
             
        