from concurrent import futures

import grpc
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
    with app.app_context():
        base_de_datos.create_all()
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
        logging.basicConfig(filename='EspotifeiRESTAPI.log', level=logging.INFO)
    for log in loggers:
        for handler in handlers:
            log.addHandler(handler)
        log.propagate = False
        log.setLevel(logging.DEBUG)

class ServidorManejadorDeArchivos:

    TIEMPO_ESPERA_CERRAR = 1000
    puerto_convertidor_archivos = 5002
    direccion_ip_convertidor_archivos = "127.0.0.1"

    def __init__(self, puerto=5001, direccion_convertidor="127.0.0.1", puerto_convertidor=5002):
        direccion_ip_convertidor_archivos = direccion_convertidor
        puerto_convertidor_archivos = puerto_convertidor
        from app.manejo_de_archivos.controlador.CancionesService import CancionesServicer
        from app.manejo_de_archivos.controlador.PortadasService import PortadasServicer
        from app.manejo_de_archivos.protos import ManejadorDeArchivos_pb2_grpc
        self.logger = logging.getLogger()
        self.puerto = puerto
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        ManejadorDeArchivos_pb2_grpc.add_CancionesServicer_to_server(CancionesServicer(), self.server)
        ManejadorDeArchivos_pb2_grpc.add_PortadasServicer_to_server(PortadasServicer(), self.server)
        self.server.add_insecure_port('[::]:' + str(self.puerto))
        self.server.add_insecure_port('0.0.0.0:' + str(self.puerto))

    def iniciar(self):
        """
        Se encarga de iniciar el servidor
        :return: None
        """
        try:
            self.server.start()
            self.logger.info("Se ha iniciado el servidor GRPC en http://0.0.0.0:" + str(self.puerto))
            self.server.wait_for_termination()
        except KeyboardInterrupt:
            self.logger.info("Se ha cerrado el servidor GRCP")

    def stop(self):
        """
        Se encarga de detener el servidor
        """
        self.server.stop(ServidorManejadorDeArchivos.TIEMPO_ESPERA_CERRAR)
        self.logger.info("Se ha cerrado el servidor GRCP")
