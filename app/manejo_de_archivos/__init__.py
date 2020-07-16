from pymongo import MongoClient
from pymongo import ASCENDING

from app import ServidorManejadorDeArchivos


class BaseDeDatosMongo:
    cliente_mongo = MongoClient(ServidorManejadorDeArchivos.direccion_ip_servidor_mongo)
    manejo_de_archivos_db = cliente_mongo['manejo_archivos']
    portadas_db = manejo_de_archivos_db['portadas']
    archivos_de_audio_db = manejo_de_archivos_db['archivos_de_audio']
    archivos_de_audio_db.create_index([('id_cancion', ASCENDING), ('calidad_audio', ASCENDING)])
    portadas_db.create_index([('id_album', ASCENDING), ('id_creador_de_contenido', ASCENDING),
                              ('id_usuario', ASCENDING), ('id_lista_de_reproduccion', ASCENDING)])

