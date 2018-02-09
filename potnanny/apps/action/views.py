from flask import render_template, redirect, request, session, \
    Blueprint, jsonify
from potnanny.extensions import db
from .models import Action, ActionProcess
from .forms import ActionForm
from potnanny.apps.outlet.models import Outlet
from potnanny.apps.measurement.models import MeasurementType
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
    if pk:
        title = 'Edit Action'
        obj = Action.query.get_or_404(pk)
        
    form = ActionForm(obj=obj)

    # populate options for measurementtype_id select fields
    form.measurement_id.choices = []
    for n in MeasurementType.query.all():
        form.measurement_id.choices.append(("%d" % n.id, n.name))  

    # populate options for outlet_id select fields
    form.outlet_id.choices = []
    for n in Outlet.query.all():
        form.outlet_id.choices.append(("%d" % n.id, n.name))

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
                        form.measurement_id.data, 
                        form.outlet_id.data, form.action_type.data)

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
    



