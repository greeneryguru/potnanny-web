from flask import render_template, redirect, request, session, Blueprint
from flask_login import login_required
from potnanny.extensions import db
from .models import Room
from .forms import RoomForm


room = Blueprint('room', __name__, template_folder='templates')


@room.route('/room')
@login_required
def room_index():
    rooms = Room.query.all()
    return render_template('room/index.html', 
                title='Rooms',
                rooms=rooms)

        
@room.route('/room/create', methods=['GET','POST'])
@room.route('/room/<pk>/edit', methods=['GET','POST'])
@login_required
def room_edit(pk=None):
    obj = None
    title = 'Add Room'

    if pk:
        title = 'Edit Room'
        obj = Room.query.get_or_404(int(pk))
        
    form = RoomForm(obj=obj)  
    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            o = Room(form.name.data)
            db.session.add(o)
    
        db.session.commit()
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/room')

    return render_template('room/form.html', 
        form=form,
        title=title,
        pk=pk)    


@room.route('/room/<pk>/delete', methods=['POST'])
@login_required
def room_delete(pk):
    o = Room.query.get_or_404(int(pk))
    db.session.delete(o)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect('/room')


