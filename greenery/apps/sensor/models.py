import os
import re
from greenery import db


class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, server_default='', unique=True)
    tags = db.Column(db.String(64), nullable=True)
    address = db.Column(db.Integer, nullable=False)

    def __init__(self, name, address, tags=None):
        self.name = name
        self.address = address
        if tags:
            self.tags = tags

    def __repr__(self):
        return self.name


