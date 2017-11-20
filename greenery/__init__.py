from flask import Flask, abort, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


# configure login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = 'strong'


# enable csrf globally
csrf = CSRFProtect(app)


# import blueprints of individual apps
from apps.admin import admin
from apps.outlet import outlet
from apps.sensor import sensor
from apps.schedule import schedule
from apps.measurement import measurement
from apps.action import action


# register blueprints
app.register_blueprint(admin)
app.register_blueprint(outlet)
app.register_blueprint(sensor)
app.register_blueprint(schedule)
app.register_blueprint(measurement)
app.register_blueprint(action)


# import views
from apps.admin import views
from apps.outlet import views
from apps.sensor import views
from apps.schedule import views
from apps.measurement import views
from apps.action import views


# import APIs
# from greenery.apps.outlet import api


# 404 error handler for API
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': '404 Not found'}), 404)


