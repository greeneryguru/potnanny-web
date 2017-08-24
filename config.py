import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = False
SECRET_KEY = 'you-will-never-guess'

# SqlAlchemy config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-User config
""" USER_ENABLE_CHANGE_PASSWORD     = True
USER_ENABLE_CONFIRM_EMAIL       = False
USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL = True
USER_ENABLE_EMAIL               = False
USER_ENABLE_REGISTRATION        = False
USER_ENABLE_RETYPE_PASSWORD     = True
USER_ENABLE_USERNAME            = True 
USER_CHANGE_PASSWORD_URL        = '/user/change-password'
USER_CHANGE_USERNAME_URL        = '/user/change-username'
USER_LOGIN_URL                  = '/user/login'
USER_LOGOUT_URL                 = '/user/logout'"""
USER_LOGIN_TEMPLATE             = 'account/login.html'
"""USER_CHANGE_PASSWORD_TEMPLATE   = 'flask_user/change_password.html'
USER_CHANGE_USERNAME_TEMPLATE   = 'flask_user/change_username.html'"""