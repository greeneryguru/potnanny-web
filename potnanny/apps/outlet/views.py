from flask import render_template, redirect, request, session, Blueprint, \
    jsonify
from flask_login import login_required
from potnanny.extensions import db
from potnanny.apps.schedule.models import Schedule
from .models import Outlet
from .forms import OutletForm


outlet = Blueprint('outlet', __name__,
                        template_folder='templates')


@outlet.route('/outlet')
@login_required
def outlet_index():
    outlets = Outlet.query.all()
    return render_template('outlet/index.html', 
                title='Outlets',
                outlets=outlets)


@outlet.route('/outlet/create', methods=['GET','POST'])
@outlet.route('/outlet/<pk>/edit', methods=['GET','POST'])
@login_required
def outlet_edit(pk=None):
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
@login_required
def outlet_delete(pk):
    o = Outlet.query.get_or_404(int(pk))
    db.session.delete(o)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect('/outlet')
    

@outlet.route('/outlet/<pk>/toggle', methods=['POST'])
@login_required
def outlet_toggle(pk):
    o = Outlet.query.get_or_404(int(pk))

    if o.state == 1 or o.state is True:
        return o.off(True)
    else:
        return o.on(True)


@outlet.route('/outlet/<pk>', methods=['GET'])
def outlet_status(pk):
    o = Outlet.query.get_or_404(int(pk))
    return str(o)


