from flask import render_template, redirect, request, session
from app import app

@app.route('/admin')
def admin_index():
    return render_template('admin/index.html', 
                title='admin')

