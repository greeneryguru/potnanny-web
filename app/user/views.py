from flask import render_template, redirect, request, session, flash
from app import app, db, login_manager
from .models import User
from .forms import LoginForm, UserForm, UserEditForm, PasswordResetForm
from flask_login import login_required, login_user, logout_user, current_user


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
            return render_template('user/login.html', 
                    form=form,
                    title=title) 

        else:
            login_user(u)

        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/')

    return render_template('user/login.html', 
            form=form,
            title=title)    
    

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/user')
@login_required
def user_index():
    users = User.query.all()
    return render_template('user/index.html', 
                title='users',
                payload=users)

        
@app.route('/user/create', methods=['GET','POST'])
@login_required
def user_create():
    title = 'new user'
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        obj = User(form.username.data)
        obj.set_password(form.password.data)
        obj.active = int(form.active.data)
        obj.email = form.email.data
        db.session.add(obj)
        db.session.commit()
        flash("create user ok")
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/user')

    return render_template('user/newuser.html', 
        form=form,
        title=title)


@app.route('/user/<pk>/edit', methods=['GET','POST'])
@login_required
def user_edit(pk):
    title = 'edit user'
    u = User.query.get_or_404(int(pk))  
    form = UserEditForm(obj=u)  
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(u)
        db.session.commit()
        flash("edit user ok")
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/user')

    return render_template('user/edit.html', 
        form=form,
        title=title,
        pk=pk)    


@app.route('/user/<pk>/delete', methods=['POST'])
@login_required
def user_delete(pk):
    u = User.query.get_or_404(int(pk))

    # nope, the admin user cannot be deleted
    if u.username == 'admin':
        flash("admin account cannot be removed")
    else:
        db.session.delete(u)
        db.session.commit()
        flash("user delete ok")

    return redirect('/user')
    

@app.route('/user/reset', methods=['GET','POST'])
@login_required
def user_reset():
    title = 'reset password'
    u = User.query.filter(User.username == current_user.username).first()
    if not u:
        pass

    form = PasswordResetForm(obj=u)
    if request.method == 'POST' and form.validate_on_submit():
        u.set_password(form.password1.data)
        db.session.commit()
        flash("password changed successfully")
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/user')

    return render_template('user/resetpass.html', 
        form=form,
        title=title)

    

