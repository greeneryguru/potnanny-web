from flask import Blueprint, render_template, redirect, request, session
from potnanny.extensions import db, login_manager, csrf
from .forms import UserForm, LoginForm, PasswordResetForm
from .models import User
from flask_login import login_required, login_user, logout_user


user = Blueprint('user', __name__, 
                 template_folder='templates')


@user.route('/user', methods=['GET'])
@login_required
def index():
    users = User.query.all()
    return render_template('user/index.html',
                title='Users',
                users=users)


@user.route('/user/create', methods=['GET','POST'])
@user.route('/user/<pk>/edit', methods=['GET','POST'])
@login_required
def edit(pk=None):
    obj = None
    title = 'Add User'

    if pk:
        title = 'Edit User'
        obj = User.query.get_or_404(int(pk))

    form = UserForm(obj=obj)
    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            u = User(form.username.data, None, form.email.data)
            db.session.add(u)

        db.session.commit()
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/user')

    return render_template('user/form.html',
        form=form,
        title=title,
        pk=pk)


@user.route('/user/<pk>/delete', methods=['POST'])
@login_required
def delete(pk):
    u = User.query.get_or_404(int(pk))
    db.session.delete(u)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect('/user')


@user.route('/user/<int:pk>/password', methods=['GET', 'POST'])
@login_required
def password_reset(pk):
    title = 'Reset Password'
    u = User.query.get(pk)
    form = PasswordResetForm(obj=u)
    if request.method == 'POST' and form.validate_on_submit():
        u.set_password(form.password.data)
        db.session.commit()
        return redirect(request.args.get("next", "/user"))

    return render_template('user/password.html', 
        form=form,
        title=title)


@login_manager.user_loader
def load_user(pk):
    try:
        u = User.query.get(int(pk))
        if u:
            return u

        return None
    except:
        return None


@user.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    title = 'Login'
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        failures = False
        u = User.query.filter(User.username == form.username.data).first()
        
        if not u:
            form.username.errors.append('invalid username')
            failures = True
            return render_template('user/login.html',
                    form=form,
                    title=title)
            
        elif not u.check_password(form.password.data):
            form.username.errors.append('incorrect password')
            failures = True
        
        if not failures:
            login_user(u)
            if request.args.get("next"):
                return redirect(request.args.get("next", "/"))
            else:
                return redirect('/')

    return render_template('user/login.html',
            form=form,
            title=title)


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')


