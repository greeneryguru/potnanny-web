from flask import render_template, redirect, request, session
from flask import jsonify
from flask_login import login_required
from greenery import app, db
from .models import Action, ActionProcess
from .forms import ActionForm
from greenery.apps.outlet.models import Outlet
from greenery.apps.measurement.models import MeasurementType
import re


@app.route('/action')
@login_required
def action_index():
    actions = Action.query.all()
    return render_template('action/index.html', 
                title='Actions',
                subtitle='automation rules',
                actions=actions)

        
@app.route('/action/create', methods=['GET','POST'])
@app.route('/action/<pk>/edit', methods=['GET','POST'])
@login_required
def action_edit(pk=None):
    obj = None
    title = 'Add Action'
    measurements = None
    outlets = None
    if pk:
        title = 'Edit Action'
        obj = Action.query.get_or_404(int(pk))
        
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
            if obj.enabled == True and form.enabled.data != True:
                # Switching an action from enabled to disabled means we need to 
                # delete any active ActionProcesses belonging to this Action.
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

            o.enabled = int(form.enabled.data)
            db.session.add(o)
    
        db.session.commit()
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/action')

    return render_template('action/form.html', 
        form=form,
        title=title,
        pk=pk)    


@app.route('/action/<pk>/delete', methods=['POST'])
@login_required
def action_delete(pk):
    o = Action.query.get_or_404(int(pk))
    db.session.delete(o)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect('/action')



