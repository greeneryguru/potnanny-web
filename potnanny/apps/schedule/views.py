from flask import render_template, redirect, request, session, \
    Blueprint, jsonify
from potnanny.extensions import db
from potnanny.utils import WeekdayMap
from potnanny.apps.outlet.models import Outlet
from flask_login import login_required
from .models import Schedule
from .forms import ScheduleForm


schedule = Blueprint('schedule', __name__,
                        template_folder='templates')


@schedule.route('/schedule')
@login_required
def schedule_index():
    schedules = Schedule.query.all()
    return render_template('schedule/index.html', 
                title='Schedules',
                subtitle='on/off timers for outlets',
                payload=schedules)

        
@schedule.route('/schedule/create', methods=['GET','POST'])
@schedule.route('/schedule/<int:pk>/edit', methods=['GET','POST'])
@login_required
def schedule_edit(pk=None):
    obj = None
    title = 'Add Schedule'
    dow = WeekdayMap(show_first=2).reverse_ordered_list()

    if pk:
        title = 'Edit Schedule'
        obj = Schedule.query.get_or_404(pk)
        
    form = ScheduleForm(obj=obj)
    form.outlet_id.choices = [(str(row.id), row.name) for row in Outlet.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            o = Schedule(
                    int(form.outlet_id.data), 
                    form.on_time.data,
                    form.off_time.data,
                    int(form.days.data),
                    int(form.custom.data)
            )

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


@schedule.route('/schedule/<int:pk>/delete', methods=['POST'])
@login_required
def schedule_delete(pk):
    o = Schedule.query.get_or_404(pk)
    db.session.delete(o)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))    
    else:
        return redirect('/schedule')
    
 
