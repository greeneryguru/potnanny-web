"""
A mixin to give our models basic REST/JSON functionality
"""
class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
