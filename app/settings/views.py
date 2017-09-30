from flask import render_template, redirect, request, session, jsonify
from flask_login import login_required
from app import app, db
from .models import Setting
from .forms import SettingForm
import datetime


@app.route('/settings')
@login_required
def settings_index():
    s = Setting.query.all()
    return render_template('settings/index.html', 
                title='settings',
                payload=s)


@app.route('/settings/<pk>/edit', methods=['GET','POST'])
@login_required
def settings_edit(pk):
    title = 'edit setting'
    obj = Setting.query.get_or_404(int(pk))    
    form = SettingForm(obj=obj)  
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(obj)
        db.session.commit()
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/settings')

    return render_template('settings/form.html', 
        form=form,
        title=title,
        pk=pk,
        setting=obj.name)    


@app.route('/settings/time')
@login_required
def settings_servertime():
    return jsonify({'servertime': datetime.datetime.now().strftime("%H:%M")})


