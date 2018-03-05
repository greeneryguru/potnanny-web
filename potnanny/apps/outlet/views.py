from flask import render_template, redirect, request, session, Blueprint, \
    jsonify
from potnanny.extensions import db
from .models import Outlet, OutletType
from .forms import OutletForm
import time


outlet = Blueprint('outlet', __name__,
                        template_folder='templates')


@outlet.route('/outlet')
def index():
    payload = None
    outlets = Outlet.query.all()
    return render_template('outlet/index.html', 
                title='Outlets',
                payload=outlets)


@outlet.route('/outlet/create', methods=['GET','POST'])
@outlet.route('/outlet/<pk>/edit', methods=['GET','POST'])
def edit(pk=None):
    obj = None
    title = 'Add Outlet'
    schedules = None

    if pk:
        title = 'Edit Outlet'
        obj = Outlet.query.get_or_404(int(pk))

    form = OutletForm(obj=obj)
    
    # populate options for outlet types
    form.outlet_type.choices = []
    types = OutletType.query.all()
    for t in types:
        form.outlet_type.choices.append((t.id, t.name))        
     
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
    

@outlet.route('/outlet/<int:id>/toggle', methods=['POST'])
def toggle(id):
    outlet = Outlet.query.get(id)
    if outlet.state == 1:
        rval = outlet.off()
    else:
        rval = outlet.on()
            
    return jsonify(outlet.as_dict())


@outlet.route('/outlet/<int:id>', methods=['GET'])
def status(id):
    outlet = Outlet.query.get(id)
    return jsonify(outlet.as_dict())
    



