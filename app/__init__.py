from flask import Flask
from flask_sqlalchemy import SQLAlchemy

base_de_datos = SQLAlchemy()


def create_app(settings_module="config.dev"):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    base_de_datos.init_app(app)
    from app.manejo_de_usuarios import manejo_de_usuarios
    app.register_blueprint(manejo_de_usuarios)
    from app.administracion_de_contenido import administracion_de_contenido
    app.register_blueprint(administracion_de_contenido)
    base_de_datos.create_all()
    return app
