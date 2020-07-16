import threading
from concurrent import futures
import signal
import grpc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

base_de_datos = SQLAlchemy()
migrate = Migrate()


def create_app(settings_module="config.dev", puerto=5001, direccion_convertidor="127.0.0.1", puerto_convertidor=5002,
               ip_servidor_mongo="127.0.0.1", iniciar_grcp_server=False):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    configure_logging(app)
    base_de_datos.init_app(app)
    migrate.init_app(app, base_de_datos)
    from app.manejo_de_usuarios import manejo_de_usuarios
    app.register_blueprint(manejo_de_usuarios)
    from app.administracion_de_contenido import administracion_de_contenido
    app.register_blueprint(administracion_de_contenido)
    if iniciar_grcp_server:
        servidor = crear_servidor_archivos(puerto, direccion_convertidor, puerto_convertidor, ip_servidor_mongo)
        signal.signal(signal.SIGINT, servidor.stop)
    register_error_handlers(app)
    with app.app_context():
        base_de_datos.create_all()
    return app

def crear_servidor_archivos(puerto, direccion_convertidor, puerto_convertidor, ip_servidor_mongo):
    servidor = ServidorManejadorDeArchivos(puerto, direccion_convertidor, puerto_convertidor, ip_servidor_mongo)
    hilo_manejador_canciones = threading.Thread(target=servidor.iniciar)
    hilo_manejador_canciones.start()
    return servidor

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
    puerto = 5001
    TIEMPO_ESPERA_CERRAR = 10
    puerto_convertidor_archivos = 5002
    direccion_ip_convertidor_archivos = "127.0.0.1"
    direccion_ip_servidor_mongo = "127.0.0.1"

    @staticmethod
    def _establecer_direcciones_servicios(puerto, direccion_convertidor, puerto_convertidor, ip_servidor_mongo):
        if puerto is not None:
            try:
                ServidorManejadorDeArchivos.puerto = int(puerto)
            except ValueError:
                ServidorManejadorDeArchivos.puerto = 5001
                print('GRPC_PORT invalido se ha asignado automaticamente el puerto 5001')
        else:
            ServidorManejadorDeArchivos.puerto = 5001
        if puerto_convertidor is not None:
            try:
                ServidorManejadorDeArchivos.puerto_convertidor_archivos = int(puerto_convertidor)
            except ValueError:
                ServidorManejadorDeArchivos.puerto_convertidor_archivos = 5002
                print('CONVERTIDOR_ARCHIVOS_PORT invalido se ha asignado automaticamente el puerto 5002')
            else:
                ServidorManejadorDeArchivos.puerto_convertidor_archivos = 5002
        ServidorManejadorDeArchivos.direccion_ip_convertidor_archivos = direccion_convertidor
        ServidorManejadorDeArchivos.direccion_ip_servidor_mongo = ip_servidor_mongo

    def __init__(self, puerto, direccion_convertidor, puerto_convertidor, ip_servidor_mongo):
        ServidorManejadorDeArchivos._establecer_direcciones_servicios(puerto, direccion_convertidor, puerto_convertidor,
                                                                      ip_servidor_mongo)
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
        except Exception as ex:
            self.logger.info(str(ex))

    def stop(self, *args):
        """
        Se encarga de detener el servidor
        """
        self.server.stop(ServidorManejadorDeArchivos.TIEMPO_ESPERA_CERRAR)
        self.logger.info("Se ha cerrado el servidor GRCP")
