from flask import render_template, redirect, request, session, Blueprint
from flask_login import login_required

help = Blueprint('help', __name__,
                        template_folder='templates')


@help.route('/help/outlet', methods=['GET'])
@login_required
def outlets():
    return render_template('help/outlets.html')