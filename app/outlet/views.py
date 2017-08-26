from flask import render_template, redirect, request, session
from flask import jsonify
from app import app, db
from .models import Outlet
from .forms import OutletForm


@app.route('/outlets')
def outlet_index():
    outlets = Outlet.query.all()
    return render_template('outlet/index.html', 
                title='Outlets',
                outlets=outlets)

        
@app.route('/outlets/create', methods=['GET','POST'])
@app.route('/outlets/<pk>/edit', methods=['GET','POST'])
def outlet_create(pk=None):
    action = 'Add'
    obj = None
    
    if pk:
        action = 'Edit'
        obj = Outlet.query.get_or_404(int(pk))
        
    form = OutletForm(obj=obj)  
    if request.method == 'POST' and form.validate_on_submit():
        if action == 'Add':
            o = Outlet(name=form.name.data, channel=int(form.channel.data))
            db.session.add(o)
        else:
            o = Outlet.query.get_or_404(int(form.id.data))
            o.name = form.name.data
            
        db.session.commit()
        return redirect('/outlets')

    return render_template('outlet/editcreate.html', 
        form=form,
        action=action,
        title=action)    


@app.route('/outlets/<pk>/delete', methods=['POST'])
def outlet_delete(pk):
    o = Outlet.query.get_or_404(int(pk))
    db.session.delete(o)
    db.session.commit()
    return redirect('/outlets')
    
         
@app.route('/outlets/<pk>/toggle', methods=['POST'])
def outlet_toggle(pk):
    exe = "/var/www/greenery/bin/rfoutlet"
    try:
        o = Outlet.query.get(int(pk))
        if o.state:
            o.state = 0
            os.system("%s %d off" % (exe, o.channel))
        else:
            os.system("%s %d on" % (exe, o.channel))
            o.state = 1
            
        db.session.commit()
        return jsonify(o.simplified())
    except:
        return jsonify({})
                    