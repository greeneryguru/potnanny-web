from flask import render_template, redirect, request, session, flash
from app import app, db, login_manager
from .models import User, Setting
from .forms import LoginForm, UserEditForm, PasswordResetForm, SettingForm
from flask_login import login_required, login_user, logout_user, current_user


## main admin page ##
#####################
@app.route('/admin')
@login_required
def admin_index():
    return render_template('admin/index.html', 
                title='admin')


## system settings pages ##
###########################
@app.route('/admin/settings')
@login_required
def settings_index():
    s = Setting.query.all()
    return render_template('admin/settings_index.html', 
                title='settings',
                payload=s)

@app.route('/admin/settings/<pk>/edit', methods=['GET','POST'])
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
            return redirect('/admin/settings')

    return render_template('admin/settings_form.html', 
        form=form,
        title=title,
        pk=pk,
        setting=obj.name)


## user login/management pages ##
#################################
@login_manager.user_loader
def load_user(pk):
    try:
        u = User.query.get(int(pk))
        if not u:
            return None
        return u
    except:
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'login'
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        u = User.query.filter(User.username == form.username.data).first()
        if not u or not u.check_password(form.password.data):
            form.username.errors.append('username or password incorrect')
            return render_template('admin/login.html', 
                    form=form,
                    title=title) 

        else:
            login_user(u)

        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/')

    return render_template('admin/login.html', 
            form=form,
            title=title)    
    
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/admin/profile', methods=['GET','POST'])
@login_required
def user_edit():
    title = 'edit profile'
    u = User.query.get(current_user.id)
    form = UserEditForm(obj=u)  
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(u)
        db.session.commit()
        flash("profile change ok")
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/admin')

    return render_template('admin/user_form.html', 
        form=form,
        title=title)

@app.route('/admin/resetpass', methods=['GET','POST'])
@login_required
def password_reset():
    title = 'reset password'
    u = User.query.get(current_user.id)
    form = PasswordResetForm(obj=u)
    if request.method == 'POST' and form.validate_on_submit():
        u.set_password(form.password.data)
        db.session.commit()
        flash("password change ok")
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/admin')

    return render_template('admin/password.html', 
        form=form,
        title=title)

    



