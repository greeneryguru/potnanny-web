from flask import render_template, redirect, request, session, \
    Blueprint, jsonify
from potnanny.extensions import db
from .models import Action, ActionProcess
from .forms import ActionForm
from sqlalchemy.orm import load_only
from potnanny.apps.outlet.models import Outlet
from potnanny.apps.measurement.models import Measurement
from potnanny.apps.sensor.models import Sensor
import re

action = Blueprint('action', __name__,
                        template_folder='templates')

@action.route('/action')
def action_index():
    actions = Action.query.all()
    return render_template('action/index.html', 
                title='Actions',
                actions=actions)

        
@action.route('/action/create', methods=['GET','POST'])
@action.route('/action/<int:pk>/edit', methods=['GET','POST'])
def action_edit(pk=None):
    obj = None
    title = 'Add Action'
    measurements = None
    outlets = None
    has_outlets = False
    if pk:
        title = 'Edit Action'
        obj = Action.query.get_or_404(pk)
        
    form = ActionForm(obj=obj)

    # populate options for measurement type select fields
    form.measurement_type.choices = []
    measurements = Measurement.query.group_by(
            Measurement.type_m).options(
                load_only("type_m")).distinct("type_m").all()
            
    for m in measurements:
        form.measurement_type.choices.append((m.type_m, m.type_m))  

    # populate options for outlet select fields
    form.outlet_id.choices = []
    try:
        my_outlets = Outlet.query.all()
        for o in my_outlets:
            has_outlets = True
            form.outlet_id.choices.append((o.id, o.name))
    except:
        pass
    
    # populate sensor data choices
    for s in list(Sensor.query.all()):
        form.sensor_address.choices.append((s.address, s.name))
    
    # populate options for action-types
    form.action_type.choices = [('sms-message', 'send message')]
    if has_outlets:
        form.action_type.choices.append(('switch-outlet', 'control outlet'))
    
    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            if obj.active == True and form.active.data != True:
                # Deactivating an action means we need to delete any 
                # active ActionProcesses belonging to this Action.
                ActionProcess.query.filter(
                    ActionProcess.action_id == obj.id
                ).delete()
                db.session.commit()

            form.populate_obj(obj)
        else:
            o = Action(form.name.data, 
                        form.measurement_type.data, 
                        form.outlet_id.data, 
                        form.sensor_address.data,
                        form.action_type.data)

            o.on_condition = form.on_condition.data
            o.on_threshold = form.on_threshold.data
                
            if re.search(r'sms', form.action_type.data, re.IGNORECASE):
                o.sms_recipient = form.sms_recipient.data
                
            if re.search(r'switch', form.action_type.data, re.IGNORECASE):
                o.off_condition = form.off_condition.data
                o.off_threshold = form.off_threshold.data

            o.active = int(form.active.data)
            db.session.add(o)
    
        db.session.commit()
        return redirect(request.args.get("next", "/action"))

    return render_template('action/form.html', 
                           form=form,
                           title=title,
                           pk=pk)    


@action.route('/action/<int:pk>/delete', methods=['POST'])
def action_delete(pk):
    o = Action.query.get_or_404(pk)
    db.session.delete(o)
    db.session.commit()
    return redirect(request.args.get("next", "/action"))
    



