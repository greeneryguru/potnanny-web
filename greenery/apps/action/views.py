from flask import render_template, redirect, request, session
from flask import jsonify
from flask_login import login_required
from greenery import app, db
from .models import Action
from .forms import ActionForm
from greenery.apps.outlet.models import Outlet
from greenery.apps.measurement.models import MeasurementType

@app.route('/action')
@login_required
def action_index():
    actions = Action.query.all()
    return render_template('action/index.html', 
                title='Actions',
                subtitle='automation rules',
                payload=actions)

        
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

    # populate options for select fields
    form.type_id.choices = []
    for n in MeasurementType.query.all():
        form.type_id.choices.append(("%d" % n.id, n.name))  

    form.outlet.choices = []
    for n in Outlet.query.all():
        form.outlet.choices.append((n.name, n.name))

    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            o = Action()
            o.type_id = int(form.type_id.data)
            o.condition = form.condition.data
            o.value = int(form.value.data)
            o.wait_time = int(form.wait_time.data)
            o.action = form.action.data
            o.action_state = int(form.action_state.data)
            o.action_target = form.action_target.data
            o.active = int(form.active.data)
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



