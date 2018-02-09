from flask import render_template, redirect, request, session, Blueprint
from potnanny.extensions import db
from .models import Sensor
from .forms import SensorForm


sensor = Blueprint('sensor', __name__, template_folder='templates')


@sensor.route('/sensor')
def sensor_index():
    sensors = Sensor.query.all()
    return render_template('sensor/index.html', 
                title='Sensors',
                sensors=sensors)

        
@sensor.route('/sensor/create', methods=['GET','POST'])
@sensor.route('/sensor/<pk>/edit', methods=['GET','POST'])
def sensor_edit(pk=None):
    obj = None
    title = 'Add Sensor'

    if pk:
        title = 'Edit Sensor'
        obj = Sensor.query.get_or_404(int(pk))
        
    form = SensorForm(obj=obj)  
    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            o = Sensor(form.name.data, form.address.data)
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


@sensor.route('/sensor/<pk>/delete', methods=['POST'])
def sensor_delete(pk):
    o = Sensor.query.get_or_404(int(pk))
    db.session.delete(o)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect('/sensor')


