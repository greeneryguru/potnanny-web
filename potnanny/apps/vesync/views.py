from flask import render_template, redirect, request, session, Blueprint
from potnanny.extensions import db
from .models import VesyncUser
from .forms import VesyncForm

vesync = Blueprint('vesync', __name__,
                        template_folder='templates')


## vesync user pages ##
#######################
@vesync.route('/vesync')
def index():
    results = VesyncUser.query.all()
    return render_template('vesync/index.html', 
                title='VeSync Account',
                payload=results)


@vesync.route('/vesync/create', methods=['GET','POST'])
@vesync.route('/vesync/<int:pk>/edit', methods=['GET','POST'])
def edit(pk=None):
    obj = None
    title = 'Create VeSync Account'

    if pk:
        title = 'Edit VeSync Account'
        obj = VesyncUser.query.get_or_404(pk)
        
    form = VesyncForm(obj=obj)  
    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            o = VesyncUser(form.username.data, form.password.data)
            db.session.add(o)
            
        db.session.commit()
        return redirect(request.args.get("next", "/vesync"))
    
    return render_template('vesync/form.html', 
        form=form,
        title=title)


@vesync.route('/vesync/<pk>/delete', methods=['POST'])
def delete(pk):
    o = VesyncUser.query.get_or_404(int(pk))
    db.session.delete(o)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect('/vesync')
