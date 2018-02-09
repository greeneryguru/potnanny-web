import os
import re
from flask import Flask, render_template, current_app
from .config import DefaultConfig
from .extensions import db, csrf, login_manager
from .utils import INSTANCE_FOLDER_PATH, BASEDIR


__all__ = ['create_app', 'initialize_database']


def create_app(config=None, app_name=None, init_db=True):

    if app_name is None:
        app_name = DefaultConfig.PROJECT

    app = Flask(app_name, instance_path=INSTANCE_FOLDER_PATH, 
                instance_relative_config=True)
    
    
    # configure all aspects of the newly created app
    configure_app(app, config)
    configure_extensions(app)
    configure_blueprints(app)
    # configure_logging(app)
    csrf.init_app(app)
    
    
    # import all required views
    from potnanny.apps.sensor import views
    from potnanny.apps.measurement import views
    from potnanny.apps.outlet import views
    from potnanny.apps.schedule import views
    from potnanny.apps.action import views
    from potnanny.apps.messenger import views
    from potnanny.apps.settings import views
    from potnanny.apps.system import views
    from potnanny.apps.help import views
    from potnanny.apps.vesync import views
    
    return app


def configure_app(app, config=None):
    app.config.from_object(DefaultConfig)
    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)


def configure_blueprints(app):
    from potnanny.apps.sensor import sensor
    from potnanny.apps.measurement import measurement
    from potnanny.apps.outlet import outlet
    from potnanny.apps.schedule import schedule
    from potnanny.apps.action import action
    from potnanny.apps.messenger import messenger
    from potnanny.apps.settings import settings
    from potnanny.apps.system import system
    from potnanny.apps.help import help
    from potnanny.apps.vesync import vesync
    
    app.register_blueprint(sensor)
    app.register_blueprint(measurement)
    app.register_blueprint(outlet)
    app.register_blueprint(schedule)
    app.register_blueprint(action)
    app.register_blueprint(messenger)
    app.register_blueprint(settings)
    app.register_blueprint(system)
    app.register_blueprint(help)
    app.register_blueprint(vesync)
    
def configure_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'


def configure_logging(app):
    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging
    import os

    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'potnanny.log')
    info_file_handler = logging.handlers.RotatingFileHandler(info_log, 
                                                             maxBytes=100000, 
                                                             backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)


def configure_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404


def configure_database(app, force=False):
    if not app.config['TESTING']:
        app.app_context().push()
    
    uri = app.config['SQLALCHEMY_DATABASE_URI']
    match = re.search(r'sqlite:///(.+)', uri)
    fname = None
    if match:
        fname = match.group(1)

    if os.path.exists(fname) and force:
        os.remove(fname)
        
    if not os.path.exists(fname):
        db.init_app(app)
        db.create_all()
        
        engine = db.engine
        connection = engine.connect()
        with current_app.open_resource('schema.sql', mode='r') as f:
            for line in f.readlines():
                
                if re.search(r'^\s*$', line):
                    continue
                
                if re.search(r'^#', line):
                    continue
                
                connection.execute(line)
            
        connection.close()    
        db.session.commit()

    