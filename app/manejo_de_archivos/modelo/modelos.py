from app.manejo_de_archivos import BaseDeDatosMongo
from app.manejo_de_archivos.modelo.enums.enums import Calidad, FormatoAudio, FormatoImagen


class ArchivoAudio(BaseDeDatosMongo):

    def __init__(self, calidad_audio, formato, ruta, hash256, tamano, id_cancion=None, id_cancion_personal=None,
                 es_original=False):
        self.id_cancion = id_cancion
        self.id_cancion_personal = id_cancion_personal
        self.calidad_audio = calidad_audio
        self.es_original = es_original
        self.formato = formato
        self.ruta = ruta
        self.hash256 = hash256
        self.tamano = tamano
        self.eliminado = False

    def guardar(self):
        """
        Se encarga de guardar el objeto actual en la base de datos
        :return: None
        """
        if self.id_cancion is not None:
            BaseDeDatosMongo.archivos_de_audio_db.insert(self._obtener_diccionario_de_atributos_cancion())
        elif self.id_cancion_personal is not None:
            BaseDeDatosMongo.archivos_de_audio_db.insert(self._obtener_diccionario_de_atributos_cancion_personal())

    def _obtener_diccionario_de_atributos_cancion(self):
        """
        Crea un diccionario con los atributos del objeto para guardar los atributos del objeto con el id_cancion
        :return: Un diccionario
        """
        diccionario = {
            'id_cancion': self.id_cancion, 'calidad_audio': self.calidad_audio.value, 'es_original': self.es_original,
            'formato': self.formato.value, 'ruta': self.ruta, 'hash256': self.hash256, 'tamano': self.tamano,
            'eliminado': self.eliminado
        }
        return diccionario

    def _obtener_diccionario_de_atributos_cancion_personal(self):
        """
        Crea un diccionario con los atributos del objeto para guardar los atributos del objeto con el
        id_cancion_personal
        :return: Un diccionario
        """
        diccionario = {
            'id_cancion_personal': self.id_cancion_personal, 'calidad_audio': self.calidad_audio.value,
            'es_original': self.es_original, 'formato': self.formato.value, 'ruta': self.ruta, 'hash256': self.hash256,
            'tamano': self.tamano, 'eliminado': self.eliminado
        }
        return diccionario

    def editar_archivo_audio(self, es_original, formato, ruta, hash256, tamano):
        """
        Edita los atributos del objeto y lo guarda en la base de datos
        :param es_original: Indica si el archivo audio pertence a la cancion original
        :param formato: El formato del archivo de audio
        :param ruta: La ruta en donde se almaceno la cancion
        :param hash256: El hash256 de la cancion
        :param tamano: El tamano en bytes de la cancion
        :return: None
        """
        self.es_original = es_original
        self.formato = formato
        self.ruta = ruta
        self.hash256 = hash256
        self.tamano = tamano
        if self.id_cancion is not None:
            BaseDeDatosMongo.archivos_de_audio_db.update(
                {'id_cancion': self.id_cancion, 'calidad_audio': self.calidad_audio.value},
                {"$set": {'es_original': self.es_original,
                          'formato': self.formato.value, 'ruta': self.ruta, 'hash256': self.hash256,
                          'tamano': self.tamano}})
        elif self.id_cancion_personal is not None:
            BaseDeDatosMongo.archivos_de_audio_db.update(
                {'id_cancion_personal': self.id_cancion, 'calidad_audio': self.calidad_audio.value},
                {"$set": {'es_original': self.es_original,
                          'formato': self.formato.value, 'ruta': self.ruta, 'hash256': self.hash256,
                          'tamano': self.tamano}})

    def eliminar(self):
        """
        Cambia el estado del archivo de audio y lo guarda en la base de datos
        :return: None
        """
        self.eliminado = True
        if self.id_cancion is not None:
            BaseDeDatosMongo.archivos_de_audio_db.update(
                {'id_cancion': self.id_cancion, 'calidad_audio': self.calidad_audio.value},
                {"$set": {'eliminado': self.eliminado}})
        elif self.id_cancion_personal is not None:
            BaseDeDatosMongo.archivos_de_audio_db.update(
                {'id_cancion_personal': self.id_cancion_personal, 'calidad_audio': self.calidad_audio.value},
                {"$set": {'eliminado': self.eliminado}})

    @staticmethod
    def _obtener_archivo_audio_de_diccionario_cancion(diccionario):
        """
        Crea un objeto de tipo archivo con la informacion del diccionario para una cancion
        :param diccionario: El diccionario del cual se va a crear el ArchivoAudio
        :return: Un objeto de tipo ArchivoAudio
        """
        if diccionario is not None:
            archivo_audio = ArchivoAudio(id_cancion=diccionario['id_cancion'],
                                         calidad_audio=Calidad(diccionario['calidad_audio']),
                                         es_original=diccionario['es_original'],
                                         formato=FormatoAudio(diccionario['formato']), ruta=diccionario['ruta'],
                                         hash256=diccionario['hash256'], tamano=diccionario['tamano'])
            return archivo_audio

    @staticmethod
    def _obtener_archivo_audio_de_diccionario_cancion_personal(diccionario):
        """
        Crea un objeto de tipo archivo con la informacion del diccionario para una cancion personal
        :param diccionario: El diccionario del cual se va a crear el ArchivoAudio
        :return: Un objeto de tipo ArchivoAudio
        """
        if diccionario is not None:
            archivo_audio = ArchivoAudio(id_cancion_personal=diccionario['id_cancion_personal'],
                                         calidad_audio=Calidad(diccionario['calidad_audio']),
                                         es_original=diccionario['es_original'],
                                         formato=FormatoAudio(diccionario['formato']), ruta=diccionario['ruta'],
                                         hash256=diccionario['hash256'], tamano=diccionario['tamano'])
            return archivo_audio

    @staticmethod
    def obtener_archivo_audio_cancion(id_cancion, calidad):
        """
        Recupera de la base de datos el ArchivoAudio con el id_cancion y la calidad
        :param id_cancion: El id de la cancion a recuperar
        :param calidad: La calidad del archivo a registrar
        :return: El archivo de audio que tiene el id_cancion y la calidad indicada
        """
        archivo_audio = BaseDeDatosMongo.archivos_de_audio_db.find_one({'id_cancion': id_cancion,
                                                                        'calidad_audio': calidad.value})
        return ArchivoAudio._obtener_archivo_audio_de_diccionario_cancion(archivo_audio)

    @staticmethod
    def obtener_archivo_audio_cancion_personal(id_cancion_personal, calidad):
        """
        Recupera de la base de datos el ArchivoAudio con el id_cancion_personal y la calidad
        :param id_cancion_personal: El id de la cancion a recuperar
        :param calidad: La calidad del archivo a registrar
        :return: El archivo de audio que tiene el id_cancion y la calidad indicada
        """
        archivo_audio = BaseDeDatosMongo.archivos_de_audio_db.find_one({'id_cancion_personal': id_cancion_personal,
                                                                        'calidad_audio': calidad.value})
        return ArchivoAudio._obtener_archivo_audio_de_diccionario_cancion_personal(archivo_audio)


class Portada:
    def __init__(self, ruta, alto, ancho, hash256, formato, calidad_imagen, id_album=None, id_creador_de_contenido=None,
                 id_usuario=None, id_lista_de_reproduccion=None, es_original=False):
        self.calidad_imagen = calidad_imagen
        self.es_original = es_original
        self.ruta = ruta
        self.alto = alto
        self.ancho = ancho
        self.hash256 = hash256
        self.formato = formato
        self.id_album = id_album
        self.id_creador_de_contenido = id_creador_de_contenido
        self.id_usuario = id_usuario
        self.id_lista_de_reproduccion = id_lista_de_reproduccion

    def guardar(self):
        """
        Se encarga de guardar el objeto actual en la base de datos
        :return: None
        """
        if self.id_album is not None:
            BaseDeDatosMongo.portadas_db.insert(self._obtener_diccionario_de_atributos_album())
        elif self.id_creador_de_contenido is not None:
            BaseDeDatosMongo.portadas_db.insert(self._obtener_diccionario_de_atributos_creador_de_contenido())
        elif self.id_usuario is not None:
            BaseDeDatosMongo.portadas_db.insert(self._obtener_diccionario_de_atributos_usuario())
        elif self.id_lista_de_reproduccion:
            BaseDeDatosMongo.portadas_db.insert(self._obtener_diccionario_de_atributos_lista_de_reproduccion())

    def _obtener_diccionario_de_atributos_album(self):
        """
        Crea un diccionario con los atributos del objeto para guardar los atributos del objeto con el id_album
        :return: Un diccionario
        """
        diccionario = {
            'id_album': self.id_album, 'calidad_imagen': self.calidad_imagen.value, 'es_original': self.es_original,
            'formato': self.formato.value, 'ruta': self.ruta, 'hash256': self.hash256, 'alto': self.alto,
            'ancho': self.ancho
        }
        return diccionario

    def _obtener_diccionario_de_atributos_creador_de_contenido(self):
        """
        Crea un diccionario con los atributos del objeto para guardar los atributos del objeto con el
        id_creador_de_contenido
        :return: Un diccionario
        """
        diccionario = {
            'id_creador_de_contenido': self.id_creador_de_contenido, 'calidad_imagen': self.calidad_imagen.value,
            'es_original': self.es_original, 'formato': self.formato.value, 'ruta': self.ruta, 'hash256': self.hash256,
            'alto': self.alto, 'ancho': self.ancho
        }
        return diccionario

    def _obtener_diccionario_de_atributos_usuario(self):
        """
        Crea un diccionario con los atributos del objeto para guardar los atributos del objeto con el id_usuario
        :return: Un diccionario
        """
        diccionario = {
            'id_usuario': self.id_usuario, 'calidad_imagen': self.calidad_imagen.value,
            'es_original': self.es_original, 'formato': self.formato.value, 'ruta': self.ruta, 'hash256': self.hash256,
            'alto': self.alto, 'ancho': self.ancho
        }
        return diccionario

    def _obtener_diccionario_de_atributos_lista_de_reproduccion(self):
        """
        Crea un diccionario con los atributos del objeto para guardar los atributos del objeto con el
        id_lista_de_reproduccion
        :return: Un diccionario
        """
        diccionario = {
            'id_lista_de_reproduccion': self.id_lista_de_reproduccion, 'calidad_imagen': self.calidad_imagen.value,
            'es_original': self.es_original, 'formato': self.formato.value, 'ruta': self.ruta, 'hash256': self.hash256,
            'alto': self.alto, 'ancho': self.ancho
        }
        return diccionario

    def editar_portada(self, es_original, formato, ruta, hash256, alto, ancho):
        """
        Edita los atributos del objeto y lo guarda en la base de datos
        :param es_original: Indica si el archivo audio pertence a la cancion original
        :param formato: El formato del archivo de audio
        :param ruta: La ruta en donde se almaceno la cancion
        :param hash256: El hash256 de la cancion
        :param alto: El alto en bytes de la imagen
        :param ancho: El ancho en bytes de la imagen
        :return: None
        """
        self.es_original = es_original
        self.formato = formato
        self.ruta = ruta
        self.hash256 = hash256
        self.alto = alto
        self.ancho = ancho
        if self.id_album is not None:
            BaseDeDatosMongo.portadas_db.update(
                {'id_album': self.id_album, 'calidad_imagen': self.calidad_imagen.value},
                {"$set": {'es_original': self.es_original, 'formato': self.formato.value, 'ruta': self.ruta,
                          'hash256': self.hash256, 'alto': self.alto, 'ancho': self.ancho}})
        elif self.id_creador_de_contenido is not None:
            BaseDeDatosMongo.portadas_db.update(
                {'id_creador_de_contenido': self.id_creador_de_contenido, 'calidad_imagen': self.calidad_imagen.value},
                {"$set": {'es_original': self.es_original, 'formato': self.formato.value, 'ruta': self.ruta,
                          'hash256': self.hash256, 'alto': self.alto, 'ancho': self.ancho}})
        elif self.id_usuario is not None:
            BaseDeDatosMongo.portadas_db.update(
                {'id_usuario': self.id_usuario, 'calidad_imagen': self.calidad_imagen.value},
                {"$set": {'es_original': self.es_original, 'formato': self.formato.value, 'ruta': self.ruta,
                          'hash256': self.hash256, 'alto': self.alto, 'ancho': self.ancho}})
        elif self.id_lista_de_reproduccion is not None:
            BaseDeDatosMongo.portadas_db.update(
                {'id_lista_de_reproduccion': self.id_lista_de_reproduccion,
                 'calidad_imagen': self.calidad_imagen.value},
                {"$set": {'es_original': self.es_original, 'formato': self.formato.value, 'ruta': self.ruta,
                          'hash256': self.hash256, 'alto': self.alto, 'ancho': self.ancho}})

    @staticmethod
    def _obtener_portada_de_diccionario_album(diccionario):
        """
        Crea un objeto de tipo portada con la informacion del diccionario para con el id_album
        :param diccionario: El diccionario del cual se va a crear la Portada
        :return: Un objeto de tipo Portada
        """
        if diccionario is not None:
            portada = Portada(id_album=diccionario['id_album'], calidad_imagen=Calidad(diccionario['calidad_imagen']),
                              es_original=diccionario['es_original'], formato=FormatoImagen(diccionario['formato']),
                              ruta=diccionario['ruta'], hash256=diccionario['hash256'], alto=diccionario['alto'],
                              ancho=diccionario['ancho'])
            return portada

    @staticmethod
    def _obtener_portada_de_diccionario_creador_de_contenido(diccionario):
        """
        Crea un objeto de tipo portada con la informacion del diccionario para con el id_creador_de_contenido
        :param diccionario: El diccionario del cual se va a crear la Portada
        :return: Un objeto de tipo Portada
        """
        if diccionario is not None:
            portada = Portada(id_creador_de_contenido=diccionario['id_creador_de_contenido'],
                              calidad_imagen=Calidad(diccionario['calidad_imagen']),
                              es_original=diccionario['es_original'], formato=FormatoImagen(diccionario['formato']),
                              ruta=diccionario['ruta'], hash256=diccionario['hash256'],
                              alto=diccionario['alto'], ancho=diccionario['ancho'])
            return portada

    @staticmethod
    def _obtener_portada_de_diccionario_usuario(diccionario):
        """
        Crea un objeto de tipo portada con la informacion del diccionario para con el id_usuario
        :param diccionario: El diccionario del cual se va a crear la portada
        :return: Un objeto de tipo Portada
        """
        if diccionario is not None:
            portada = Portada(id_usuario=diccionario['id_usuario'],
                              calidad_imagen=Calidad(diccionario['calidad_imagen']),
                              es_original=diccionario['es_original'], formato=FormatoImagen(diccionario['formato']),
                              ruta=diccionario['ruta'], hash256=diccionario['hash256'], alto=diccionario['alto'],
                              ancho=diccionario['ancho'])
            return portada

    @staticmethod
    def _obtener_portada_de_diccionario_lista_de_reproduccion(diccionario):
        """
        Crea un objeto de tipo portada con la informacion del diccionario para con el id_lista_de_reproduccion
        :param diccionario: El diccionario del cual se va a crear la Portada
        :return: Un objeto de tipo Portada
        """
        if diccionario is not None:
            portada = Portada(id_lista_de_reproduccion=diccionario['id_lista_de_reproduccion'],
                              calidad_imagen=Calidad(diccionario['calidad_imagen']),
                              es_original=diccionario['es_original'], formato=FormatoImagen(diccionario['formato']),
                              ruta=diccionario['ruta'], hash256=diccionario['hash256'], alto=diccionario['alto'],
                              ancho=diccionario['ancho'])
            return portada

    @staticmethod
    def obtener_portada_album(id_album, calidad):
        """
        Recupera de la base de datos la Portada con el id_album y la calidad
        :param id_album: El id de la portada a recuperar
        :param calidad: La calidad de la portada a recuperar
        :return: La portada con el id_album y la calidad
        """
        portada = BaseDeDatosMongo.portadas_db.find_one({'id_album': id_album, 'calidad_imagen': calidad.value})
        return Portada._obtener_portada_de_diccionario_album(portada)

    @staticmethod
    def obtener_portada_creador_de_contenido(id_creador_de_contenido, calidad):
        """
        Recupera de la base de datos la Portada con el id_album y la calidad
        :param id_creador_de_contenido: El id de la portada a recuperar
        :param calidad: La calidad de la portada a recuperar
        :return: La portada con el id_album y la calidad
        """
        portada = BaseDeDatosMongo.portadas_db.find_one({'id_creador_de_contenido': id_creador_de_contenido,
                                                         'calidad_imagen': calidad.value})
        return Portada._obtener_portada_de_diccionario_creador_de_contenido(portada)

    @staticmethod
    def obtener_portada_usuario(id_usuario, calidad):
        """
        Recupera de la base de datos la Portada con el id_album y la calidad
        :param id_usuario: El id de la portada a recuperar
        :param calidad: La calidad de la portada a recuperar
        :return: La portada con el id_album y la calidad
        """
        portada = BaseDeDatosMongo.portadas_db.find_one({'id_usuario': id_usuario, 'calidad_imagen': calidad.value})
        return Portada._obtener_portada_de_diccionario_usuario(portada)
