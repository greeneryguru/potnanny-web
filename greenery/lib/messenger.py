import twilio
from greenery.apps.admin.models import TwilioAccount
from twilio.rest import Client

class Messenger():
    def __init__(self, pk=1):
        self.account = TwilioAccount.query.get(pk)
        if not self.account:
            return None

        self.client = Client(self.account.sid, self.account.token)


    def message(self, recipient, message):
        number = self.account.number
        if not number:
            number = self.client.api.account.incoming_phone_numbers.create(phone_number="+15005550006")
            
        self.client.api.account.messages.create(
            to=recipient,
            from_=number,
            body=message)
            
    
        
