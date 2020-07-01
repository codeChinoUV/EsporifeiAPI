from app.manejo_de_archivos.modelo.modelos import Portada
from app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 import Calidad
from app.manejo_de_archivos.controlador.ManejadorDeArchivos import ManejadorDeArchivos


class ManejadorDePortadas:

    @staticmethod
    def validar_existe_portada_usuario_original(id_usuario):
        portada = Portada.obtener_portada_usuario(id_usuario, Calidad.ORIGINAL)
        return portada is not None

    @staticmethod
    def validar_existe_portada_usuario(id_usuario, calidad):
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        portada = Portada.obtener_portada_usuario(id_usuario, calidad)
        return portada is not None

    @staticmethod
    def validar_existe_portada_creador_de_contenido_original(id_creador_de_contenido):
        portada = Portada.obtener_portada_creador_de_contenido(id_creador_de_contenido, Calidad.ORIGINAL)
        return portada is not None

    @staticmethod
    def validar_existe_portada_creador_de_contenido(id_creador_de_contenido, calidad):
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        portada = Portada.obtener_portada_creador_de_contenido(id_creador_de_contenido, calidad)
        return portada is not None

    @staticmethod
    def validar_existe_portada_album_original(id_album):
        portada = Portada.obtener_portada_album(id_album, Calidad.ORIGINAL)
        return portada is not None

    @staticmethod
    def validar_existe_portada_album(id_album, calidad):
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        portada = Portada.obtener_portada_album(id_album, calidad)
        return portada is not None
