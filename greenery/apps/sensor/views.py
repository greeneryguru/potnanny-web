from flask import render_template, redirect, request, session
from greenery import app, db
from .models import Sensor
from .forms import SensorForm
from greenery.apps.measurement.models import Measurement
import datetime

@app.route('/sensor')
def sensor_index():
    payload = None
    now = datetime.datetime.now()
    past = now - datetime.timedelta(minutes=60)
    sensors = Sensor.query.all()
    for s in sensors:
        dataset = [s.id, s.name, None, [], {}]
        
        results = Measurement.query.filter(Measurement.sensor_id == s.id, Measurement.date_time > past).order_by(Measurement.date_time.asc())
        for r in results:
            if datetime.datetime.strftime(r.date_time, "%m/%d/%y %H:%M") not in dataset[3]:
                dataset[3].append(datetime.datetime.strftime(r.date_time, "%m/%d/%y %H:%M"))

            if r.code not in dataset[4]:
                dataset[4][r.code] = []

            dataset[4][r.code].append(r.value)

        if not payload:
            payload = []

        payload.append(dataset)

    print(payload)
    return render_template('sensor/index.html', 
                title='sensors',
                payload=payload)

        
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
    

