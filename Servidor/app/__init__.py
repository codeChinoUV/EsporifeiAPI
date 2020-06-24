from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

base_de_datos = SQLAlchemy()
migrate = Migrate()


def create_app(settings_module="config.dev"):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    configure_logging(app)
    base_de_datos.init_app(app)
    migrate.init_app(app, base_de_datos)
    from app.manejo_de_usuarios import manejo_de_usuarios
    app.register_blueprint(manejo_de_usuarios)
    from app.administracion_de_contenido import administracion_de_contenido
    app.register_blueprint(administracion_de_contenido)
    # Custom error handlers
    register_error_handlers(app)
    return app


def register_error_handlers(app):
    @app.errorhandler(500)
    def base_error_handler(e):
        return {}, 500

    @app.errorhandler(404)
    def error_404_handler(e):
        return {}, 404


def configure_logging(app):
    del app.logger.handlers[:]
    loggers = [app.logger, ]
    handlers = []
    console_handler = logging.StreamHandler()
    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        logging.basicConfig(filename='EspotifeiRESTAPI.log', level=logging.DEBUG)
    for log in loggers:
        for handler in handlers:
            log.addHandler(handler)
        log.propagate = False
        log.setLevel(logging.DEBUG)
