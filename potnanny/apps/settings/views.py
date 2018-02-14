from flask import render_template, redirect, request, session, Blueprint
from potnanny.extensions import db
from .models import Setting
from .forms import SettingForm

settings = Blueprint('settings', __name__,
                        template_folder='templates')


@settings.route('/settings', methods=['GET','POST'])
@settings.route('/settings/<int:pk>/edit', methods=['GET','POST'])
def edit(pk=1):
    title = 'System Settings'
    obj = Setting.query.get_or_404(pk)    
    form = SettingForm(obj=obj)  
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(obj)
        db.session.commit()
        return redirect(request.args.get("next", "/"))
    
    return render_template('settings/form.html', 
        form=form,
        title=title,
        pk=pk)
