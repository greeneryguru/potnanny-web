from flask import render_template, redirect, request, session, \
    Blueprint, jsonify

system = Blueprint('system', __name__,
                        template_folder='templates')

## main admin page ##
#####################
@system.route('/system')
def index():
    return render_template('system/index.html', 
                title='System Settings')


