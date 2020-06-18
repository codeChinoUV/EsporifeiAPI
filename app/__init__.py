from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

base_de_datos = SQLAlchemy()
migrate = Migrate()


def create_app(settings_module="config.dev"):
    app = Flask(__name__)
    app.config.from_object(settings_module)
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
