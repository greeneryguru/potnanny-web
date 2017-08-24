from flask import render_template, redirect, request, session, jsonify
from flask_user import current_user, login_required
from app import app, db
from .models import User
# from .forms import UserForm


@app.route('/users')
@login_required
def user_index():
    users = User.query.all()
    return render_template('user/index.html', 
                title='Users',
                users=users)

 