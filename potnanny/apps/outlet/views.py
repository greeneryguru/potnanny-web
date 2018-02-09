from flask import render_template, redirect, request, session, Blueprint, \
    jsonify
from potnanny.extensions import db
from potnanny.apps.vesync.models import VesyncUser, VesyncApi
import time


outlet = Blueprint('outlet', __name__,
                        template_folder='templates')


@outlet.route('/outlet')
def index():
    payload = None
    user = VesyncUser.query.get(1)
    if user:
        api = VesyncApi(user.username, user.password)
        payload = api.get_devices()
        
    return render_template('outlet/index.html', 
                title='Voltson Outlets',
                payload=payload)


@outlet.route('/outlet/create', methods=['GET','POST'])
@outlet.route('/outlet/<pk>/edit', methods=['GET','POST'])
def edit(pk=None):
    obj = None
    title = 'Add Outlet'
    schedules = None

    if pk:
        title = 'Edit Outlet'
        obj = Outlet.query.get_or_404(int(pk))
        schedules = Schedule.query.filter(
            Schedule.outlet_id == pk
        ).all()

    form = OutletForm(obj=obj)  
    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            o = Outlet(form.name.data, int(form.channel.data))
            db.session.add(o)
    
        db.session.commit()
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/outlet')

    return render_template('outlet/form.html', 
        form=form,
        title=title,
        schedules=schedules,
        pk=pk)    


@outlet.route('/outlet/<pk>/delete', methods=['POST'])
def delete(pk):
    o = Outlet.query.get_or_404(int(pk))
    db.session.delete(o)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect('/outlet')
    

@outlet.route('/outlet/<id>/toggle', methods=['POST'])
def toggle(id):
    user = VesyncUser.query.get(1)
    if user:
        api = VesyncApi(user.username, user.password)
        devices = api.get_devices()
        for d in devices:
            if d['id'] == id:
                if d['relay'] == 'open':
                    api.turn_off(d['id'])
                else:
                    api.turn_on(d['id'])

                return status(id, api)


@outlet.route('/outlet/<id>', methods=['GET'])
def status(id, api=None):
    if not api:
        user = VesyncUser.query.get(1)
        api = VesyncApi(user.username, user.password)
    
    devices = api.get_devices()
    for d in devices:
        if d['id'] == id:
            return jsonify(d)

    return None
    



