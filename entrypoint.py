# Por ejemplo, APP_SETTINGS_MODULE = config.prod
import os
import threading

from app import create_app, ServidorManejadorDeArchivos
settings_module = os.getenv('APP_SETTINGS_MODULE')
port_api_rest = os.getenv('PORT_API_REST')
port_grpc = os.getenv('PORT_GRPC')
app = create_app(settings_module)


if __name__ == '__main__':
    if port_api_rest is not None:
        try:
            port_api_rest = int(port_api_rest)
        except ValueError:
            print('PORT_API_REST invalido')
            port_api_rest = 5000
    else:
        port_api_rest = 5000
    if port_grpc is not None:
        try:
            port_grpc = int(port_grpc)
        except ValueError:
            port_grpc = 5001
            print('PORT_GRPC invalido')
    else:
        port_grpc = 5001

    servidor = ServidorManejadorDeArchivos(port_grpc)
    try:
        hilo_manejador_canciones = threading.Thread(target=servidor.iniciar)
        hilo_manejador_canciones.start()
        app.run(port=port_api_rest)
        print("Cerrando servidor")
        servidor.stop()
    except KeyboardInterrupt:
        print("Key")
