from flask import Flask, abort, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
serial_port = '/dev/ttyUSB0'


# configure login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
# login_manager.session_protection = 'strong'


# enable csrf globally
csrf = CSRFProtect(app)


# import blueprints of individual apps
from greenery.apps.admin import admin
from greenery.apps.outlet import outlet
from greenery.apps.sensor import sensor
from greenery.apps.schedule import schedule
from greenery.apps.measurement import measurement
from greenery.apps.action import action


# register blueprints
app.register_blueprint(admin)
app.register_blueprint(outlet)
app.register_blueprint(sensor)
app.register_blueprint(schedule)
app.register_blueprint(measurement)
app.register_blueprint(action)


# import views
from greenery.apps.admin import views
from greenery.apps.outlet import views
from greenery.apps.sensor import views
from greenery.apps.schedule import views
from greenery.apps.measurement import views
from greenery.apps.action import views


# import APIs
# from greenery.apps.outlet import api


# 404 error handler for API
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': '404 Not found'}), 404)


