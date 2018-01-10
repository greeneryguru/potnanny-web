import os
import tempfile
from .utils import INSTANCE_FOLDER_PATH, BASEDIR


class BaseConfig(object):
    PROJECT = "potnanny"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'super secret key'
    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')
    CRYPTO_CONTEXT_SCHEMES = ['bcrypt']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'sqlite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = True
    USERNAME = 'admin'
    PASSWORD = 'admin123'
    
    
class DefaultConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    

class DebugConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    
    
class TestConfig(BaseConfig):
    TESTING = True
    LOGIN_DISABLED = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + tempfile.mkstemp()[-1]
    
