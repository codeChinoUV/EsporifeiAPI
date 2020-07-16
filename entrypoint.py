# Por ejemplo, APP_SETTINGS_MODULE = config.prod
import os

from app import create_app
settings_module = os.getenv('APP_SETTINGS_MODULE')
port_grpc = os.getenv('GRPC_PORT')
ip_mongod_server = os.getenv('MONGO_IP')
ip_convertidor_archivos = os.getenv('CONVERTIDOR_ARCHIVOS_IP')
port_convertidor_archivos = os.getenv('CONVERTIDOR_ARCHIVOS_PORT')
app = create_app(settings_module, puerto_convertidor=port_convertidor_archivos,
                 direccion_convertidor=ip_convertidor_archivos, puerto=port_grpc, ip_servidor_mongo=ip_mongod_server,
                 iniciar_grcp_server=True)
