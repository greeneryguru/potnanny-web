from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_user import UserManager, SQLAlchemyAdapter
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)

# Import REST APIs
# import outlet.api
# import account.api

# Import Views
from outlet import views
from account import views

# Setup Flask-User
from account.models import User
dba = SQLAlchemyAdapter(db, User)           # Register the User model
user_manager = UserManager(dba, app)        # Initialize Flask-User