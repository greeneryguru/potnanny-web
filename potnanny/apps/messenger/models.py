from potnanny.extensions import db
import twilio
from twilio.rest import Client


class TwilioAccount(db.Model):
    __tablename__ = 'twilio_settings'
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(48), nullable=True)
    token = db.Column(db.String(48), nullable=True)
    number = db.Column(db.String(32), nullable=True)

    def __init__(self, sid, token, num):
        self.sid = sid
        self.token = token
        self.number = num

    def __repr__(self):
        return "%s/%s/%s" % (self.sid, self.token, self.number)


class Messenger():
    def __init__(self):
        self.account = TwilioAccount.query.first()
        if not self.account:
            return None

        self.client = Client(self.account.sid, self.account.token)


    def message(self, recipient, message="test message"):
        try:    
            msg = self.client.api.account.messages.create(
                to=recipient,
                from_=self.account.number,
                body=message)
            if msg.sid:
                return 0
        except:
            pass
        
        return 1
    
