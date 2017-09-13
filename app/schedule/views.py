from flask import render_template, redirect, request, session
from flask import jsonify
from app import app, db
from flask_login import login_required
from .models import Schedule
from .forms import ScheduleForm
from app.outlet.models import Outlet
from app.lib.greenery.utils import WeekdayMap


@app.route('/schedule')
@login_required
def schedule_index():
    schedules = Schedule.query.all()
    return render_template('schedule/index.html', 
                title='schedules',
                payload=schedules)

        
@app.route('/schedule/create', methods=['GET','POST'])
@app.route('/schedule/<pk>/edit', methods=['GET','POST'])
@login_required
def schedule_edit(pk=None):
    obj = None
    title = 'add schedule'
    dow = WeekdayMap(show_first=2).reverse_ordered_list()

    if pk:
        title = 'edit schedule'
        obj = Schedule.query.get_or_404(int(pk))
        
    form = ScheduleForm(obj=obj)
    form.outlet_id.choices = [(str(row.id), row.name) for row in Outlet.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            o = Schedule()
            o.outlet_id = int(form.outlet_id.data)
            o.on_time = form.on_time.data
            o.off_time = form.off_time.data
            o.days = int(form.days.data)
            db.session.add(o)
    
        db.session.commit()
        if request.args.get("next"):
            return redirect(request.args.get("next"))    
        else:
            return redirect('/schedule')

    return render_template('schedule/form.html', 
        form=form,
        title=title,
        dow=dow,
        pk=pk)    


@app.route('/schedule/<pk>/delete', methods=['POST'])
@login_required
def schedule_delete(pk):
    o = Outlet.query.get_or_404(int(pk))
    db.session.delete(o)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))    
    else:
        return redirect('/schedule')
    
 
