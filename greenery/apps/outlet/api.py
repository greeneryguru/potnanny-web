from flask import jsonify
from greenery import app, db
from .models import Outlet


@app.route('/api/outlets', methods=['GET'])
def api_outlet():
    results = {'outlets': []}
    outlets = Outlet.query.all()
    for o in outlets: 
        results['outlets'].append(o.as_dict())

    return jsonify(results)


@app.route('/api/outlets/<int:pk>', methods=['GET'])
def api_outlet_get(pk):
    o = Outlet.query.get_or_404(pk)
    return jsonify({'outlet': o.as_dict()})


@app.route('/api/outlets/<int:pk>', methods=['POST'])
@csrf.exempt
def api_outlet_update(pk):
    o = Outlet.query.get_or_404(pk)
    return jsonify({'outlet': o.as_dict()})


@app.route('/api/outlets/<int:pk>', methods=['DELETE'])
@csrf.exempt
def api_outlet_delete(pk):
    o = Outlet.query.get_or_404(pk)
    db.session.delete(o)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/outlets', methods=['POST'])
@csrf.exempt
def api_outlet_create():
    if not request.json or not 'name' in request.json or not 'channel' in request.json:
        abort(400)
    
    o = Outlet(request.json.name, int(request.json.channel))
    db.session.add(o)
    db.session.commit()
    return jsonify({'outlet': o.as_dict()})


@app.route('/api/outlets/<int:pk>/toggle', methods=['POST'])
@csrf.exempt
def api_outlet_toggle(pk):
    o = Outlet.query.get_or_404(pk)
    if o.state == 1 or o.state is True:
        rval = o.off()
        o.state = 0
    else:
        rval = o.on()
        o.state = 1

    if rval:
        return jsonify({'error': 'outlet state change failure %d' % rval})
    
    db.session.commit()
    return jsonify(o.as_dict())





