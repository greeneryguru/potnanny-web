from flask import render_template, redirect, request, session
from flask import jsonify
from app import app, db
from .models import Device, TxPwr433
from .forms import DeviceForm

@app.route('/device')
def device_index():
    d = Device.query.all()
    return render_template('device/index.html', 
                title='devices',
                payload=d)
        
@app.route('/device/<pk>/delete', methods=['POST'])
def device_delete(pk):
    o = Device.query.get_or_404(int(pk))
    db.session.delete(o)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect('/device')

@app.route('/device/create', methods=['GET','POST'])
@app.route('/device/<pk>/edit', methods=['GET','POST'])
def outlet_edit(pk=None):
    obj = None
    title = 'add device'

    if pk:
        title = 'edit device'
        obj = Device.query.get_or_404(int(pk))
        
    form = DeviceForm(obj=obj)
    presubmit_populate(form, obj)

    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            postsubmit_populate(form, obj)
            form.populate_obj(obj)
            
        else:
            parent = Device(form.name.data)
            parent.interface = child
            db.session.add(parent)       
                
        db.session.commit()
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/device')

    return render_template('device/form.html', 
        form=form,
        title=title,
        pk=pk)    


def presubmit_populate(form, obj):
    if obj:
        if obj.interface_type == 'TxPwr433':
            form.channel.data = obj.interface.channel        
  
    return

def postsubmit_populate(form, obj):
    child = None
    if obj:
        if obj.interface_type == 'TxPwr433':
            obj.interface.channel = int(form.channel.data)
      
    else:
        if obj.interface_type == 'TxPwr433':
            child = TxPwr433(int(form.channel.data))
            db.session.add(child)

    db.session.commit()    
    return child


def child_from_form(form, obj):
    child = None
    if not obj:
        if form.interface_type.data == 'TxPwr433':
            child = TxPwr433(int(form.channel.data))
            db.session.add(child)

    else:
        child = obj.interface
        if form.interface_type == 'TxPwr433':
            if int(form.channel.data) != child.channel:
                child.channel = int(form.channel.data)


    db.session.commit()
    return child   




    


