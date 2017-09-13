from flask import render_template, redirect, request, session
from app import app, db
from .models import Sensor
from .forms import SensorForm


@app.route('/sensor')
def sensor_index():
    sensors = Sensor.query.all()
    return render_template('sensor/index.html', 
                title='sensors',
                payload=sensors)

        
@app.route('/sensor/create', methods=['GET','POST'])
@app.route('/sensor/<pk>/edit', methods=['GET','POST'])
def sensor_edit(pk=None):
    obj = None
    title = 'add sensor'

    if pk:
        title = 'edit sensor'
        obj = Sensor.query.get_or_404(int(pk))
        
    form = SensorForm(obj=obj)  
    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            o = Sensor(form.name.data)
            db.session.add(o)
    
        db.session.commit()
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/sensor')

    return render_template('sensor/form.html', 
        form=form,
        title=title,
        pk=pk)    


@app.route('/sensor/<pk>/delete', methods=['POST'])
def sensor_delete(pk):
    o = Sensor.query.get_or_404(int(pk))
    db.session.delete(o)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect('/sensor')
    

