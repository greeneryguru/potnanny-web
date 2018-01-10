from flask import render_template, redirect, request, session, Blueprint
from flask_login import login_required

system = Blueprint('system', __name__,
                        template_folder='templates')

## main admin page ##
#####################
@system.route('/system')
@login_required
def index():
    return render_template('system/index.html', 
                title='System Settings')

