from flask import Flask, abort
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
# login_manager.session_protection = 'strong'


# enable csrf globally
csrf = CSRFProtect(app)


# import blueprints of individual apps
from app.admin import admin
from app.outlet import outlet
from app.schedule import schedule

# register blueprints
app.register_blueprint(admin)
app.register_blueprint(outlet)
app.register_blueprint(schedule)

# import views
from app.admin import views
from app.outlet import views
from app.schedule import views


