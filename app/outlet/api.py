from app import app, api, db
from flask import abort, request
from flask_restful import Resource
from .models import Outlet

## Outlet REST API ##
class OutletListAPI(Resource):
    def get(self):
        try:
            r = []
            objs = Outlet.query.all()
            for o in objs:
                r.append(o.simplified())    
            return r
        except:
            abort(404)

    def put(self):
        try: 
            o = Outlet(name=request.form['name'])
            db.session.add(o)
            db.session.commit()
            return o.simplified()
        except:
            abort(404)          

class OutletAPI(Resource):
    def get(self, pk):
        try:
            o = Outlet.query.get(int(pk))
            return o.simplified()
        except:
            abort(404)
            
    def delete(self, pk):
        try:
            o = Outlet.query.get(pk)
            db.session.delete(o)
            db.session.commit()
            return {}
        except:
            abort(404)

api.add_resource(OutletListAPI, '/api/outlets')
api.add_resource(OutletAPI, '/api/outlets/<pk>')
