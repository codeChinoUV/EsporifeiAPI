import threading
from concurrent.futures.thread import ThreadPoolExecutor

from app.manejo_de_archivos.clientes_convertidor_archivos.enums.TipoPortada import TipoPortada
from app.manejo_de_archivos.manejador_de_archivos.ManejadorCanciones import ManejadorCanciones
from app.manejo_de_archivos.manejador_de_archivos.MenejadorDePortadas import ManejadorDePortadas


class ConvertidorDeArchivos:
    _cantidad_hilos_ejecutandose = 0
    _cola_convertidor_portadas_album = []
    _portada_album_actual_convirtiendo = 0
    _cola_convertidor_portadas_creador_de_contendio = []
    _portada_creador_de_contenido_actual_convirtiendo = 0
    _cola_convertidor_portadas_usuario = []
    _portada_usuario_actual_convirtiendo = 0
    _cola_convertidor_canciones = []
    _cancion_actual_convirtiendo = 0
    _cola_convertidor_canciones_personales = []
    _cancion_personal_actual_convirtiendo = 0
    _executor = ThreadPoolExecutor(max_workers=5)
    _lock = threading.Lock()
    __convertidor_de_archivos = None

    def __new__(cls):
        if ConvertidorDeArchivos.__convertidor_de_archivos is None:
            ConvertidorDeArchivos.__convertidor_de_archivos = object.__new__(cls)
        return ConvertidorDeArchivos.__convertidor_de_archivos

    def agregar_portada_album_a_cola(self, id_album):
        """
        Agrega una portada a la cola de convertir archivos
        :param id_album: El id del album a agregar a la cola
        :return: None
        """
        if id_album not in ConvertidorDeArchivos._cola_convertidor_portadas_album:
            ConvertidorDeArchivos._cola_convertidor_portadas_album.append(id_album)
            if ConvertidorDeArchivos._cantidad_hilos_ejecutandose < 5 and \
                    ConvertidorDeArchivos._portada_album_actual_convirtiendo == 0:
                self._crear_hilo_convertir_portada_album()

    def agregar_portada_creador_de_contenido_a_cola(self, id_creador_de_contenido):
        """
        Agrega una portada a la cola de convertir archivos
        :param id_creador_de_contenido: El id del creador de contenido a agregar a la cola
        :return: None
        """
        if id_creador_de_contenido not in ConvertidorDeArchivos._cola_convertidor_portadas_creador_de_contendio:
            ConvertidorDeArchivos._cola_convertidor_portadas_creador_de_contendio.append(id_creador_de_contenido)
            if ConvertidorDeArchivos._cantidad_hilos_ejecutandose < 5 and \
                    ConvertidorDeArchivos._portada_creador_de_contenido_actual_convirtiendo == 0:
                self._crear_hilo_convertir_portada_creador_de_contenido()

    def agregar_porada_usuario_a_cola(self, id_usuario):
        """
        Agrega una portada a la cola de convertir archivos
        :param id_usuario: El id del usuario a agregar a la cola
        :return: None
        """
        if id_usuario not in ConvertidorDeArchivos._cola_convertidor_portadas_usuario:
            ConvertidorDeArchivos._cola_convertidor_portadas_usuario.append(id_usuario)
            if ConvertidorDeArchivos._cantidad_hilos_ejecutandose < 5 and \
                    ConvertidorDeArchivos._portada_usuario_actual_convirtiendo == 0:
                self._crear_hilo_convertir_portada_usuario()

    def agregar_cancion_a_cola(self, id_cancion):
        """
        Agrega una cancion a la cola de convertir archivos
        :param id_cancion: El id de la cancion a agregar a la cola
        :return: None
        """
        if id_cancion not in ConvertidorDeArchivos._cola_convertidor_canciones:
            ConvertidorDeArchivos._cola_convertidor_canciones.append(id_cancion)
            if ConvertidorDeArchivos._cantidad_hilos_ejecutandose < 5 and \
                    ConvertidorDeArchivos._cancion_actual_convirtiendo == 0:
                self._crear_hilo_convertir_cancion()

    def agregar_cancion_personal_a_cola(self, id_cancion_personal):
        """
        Agrega una cancionPersonal a la cola de convertir archivos
        :param id_cancion_personal: El id de la cancion personal a agregar a la cola
        :return: None
        """
        if id_cancion_personal not in ConvertidorDeArchivos._cola_convertidor_canciones_personales:
            ConvertidorDeArchivos._cola_convertidor_canciones_personales.append(id_cancion_personal)
            if ConvertidorDeArchivos._cantidad_hilos_ejecutandose < 5 and \
                    ConvertidorDeArchivos._cancion_personal_actual_convirtiendo == 0:
                self._crear_hilo_convertir_cancion_personal()

    def _convertir_cancion(self, id_cancion):
        """
        Llama al metodo de convertir cancion y la quita de la cola cuando el metodo se termina de convertir
        :param id_cancion: El id de la cancion a convertir
        :return: None
        """
        ManejadorCanciones.convertir_cancion_mp3_todas_calidades(id_cancion)
        self._quitar_de_cola_canciones()

    def _convertir_cancion_personal(self, id_cancion_personal):
        """
        Llama al metodo de convertir cancion_personal y la quita de la cola cuando el metodo se termina de convertir
        :param id_cancion_personal: El id de la cancion personal a convertir
        :return: None
        """
        ManejadorCanciones.convertir_cancion_personal_mp3_todas_calidades(id_cancion_personal)
        self._quitar_de_cola_canciones_personales()

    def _convertir_portada_album(self, id_album):
        """
        Llama al metodo de convertir portada y la quita de la cola cuando el metodo se termina de convertir
        :param id_album: El id del album a convertir
        :return: None
        """
        ManejadorDePortadas.convertir_portada_todas_calidades(id_album, TipoPortada.ALBUM)
        self._quitar_de_cola_portada_album()

    def _convertir_portada_creador_de_contenido(self, id_creador_de_contenido):
        """
        Llama al metodo de convertir convertir portada y la quita de la cola cuando el metodo se termina de convertir
        :param id_creador_de_contenido: El id del creador de contenido a convertir
        :return: None
        """
        ManejadorDePortadas.convertir_portada_todas_calidades(id_creador_de_contenido, TipoPortada.CREADOR_DE_CONTENIDO)
        self._quitar_de_cola_portada_creadores_de_contenido()

    def _convertir_portada_usuario(self, id_usuario):
        """
        Llama al metodo de convertir portada y la quita de la cola cuando el metodo se termina de convertir
        :param id_usuario: El id del usuario a convertir
        :return: None
        """
        ManejadorDePortadas.convertir_portada_todas_calidades(id_usuario, TipoPortada.USUARIO)
        self._quitar_de_cola_portada_usuario()

    def _quitar_de_cola_canciones(self):
        """
        Quita la primera cancion de la cola
        """
        with ConvertidorDeArchivos._lock:
            ConvertidorDeArchivos._cola_convertidor_canciones.pop()
            ConvertidorDeArchivos._cantidad_hilos_ejecutandose -= 1
            ConvertidorDeArchivos._cancion_actual_convirtiendo = 0
        if len(ConvertidorDeArchivos._cola_convertidor_canciones) > 0 and \
                ConvertidorDeArchivos._cancion_actual_convirtiendo == 0:
            self._crear_hilo_convertir_cancion()

    def _crear_hilo_convertir_cancion(self):
        """
        Crea un hilo para convertir una cancion
        """
        ConvertidorDeArchivos._executor.submit(self._convertir_cancion,
                                               ConvertidorDeArchivos._cola_convertidor_canciones[0])
        ConvertidorDeArchivos._cancion_actual_convirtiendo = ConvertidorDeArchivos._cola_convertidor_canciones[0]
        ConvertidorDeArchivos._cantidad_hilos_ejecutandose += 1

    def _crear_hilo_convertir_cancion_personal(self):
        """
        Crea un hilo para convertir una cancion personal
        """
        ConvertidorDeArchivos._executor.submit(self._convertir_cancion_personal,
                                               ConvertidorDeArchivos._cola_convertidor_canciones_personales[0])
        ConvertidorDeArchivos._cancion_personal_actual_convirtiendo = \
            ConvertidorDeArchivos._cola_convertidor_canciones_personales[0]
        ConvertidorDeArchivos._cantidad_hilos_ejecutandose += 1

    def _quitar_de_cola_canciones_personales(self):
        """
        Quita la primera cancion personal de la cola
        """
        with ConvertidorDeArchivos._lock:
            ConvertidorDeArchivos._cola_convertidor_canciones_personales.pop()
            ConvertidorDeArchivos._cantidad_hilos_ejecutandose -= 1
            ConvertidorDeArchivos._cancion_personal_actual_convirtiendo = 0
            if len(ConvertidorDeArchivos._cola_convertidor_canciones_personales) > 0 and \
                    ConvertidorDeArchivos._cancion_personal_actual_convirtiendo == 0:
                self._crear_hilo_convertir_cancion_personal()

    def _crear_hilo_convertir_portada_album(self):
        """
        Crea un hilo para convertir una portada album
        """
        ConvertidorDeArchivos._executor.submit(self._convertir_portada_album,
                                               ConvertidorDeArchivos._cola_convertidor_portadas_album[0])
        ConvertidorDeArchivos._portada_album_actual_convirtiendo = \
            ConvertidorDeArchivos._cola_convertidor_portadas_album[0]
        ConvertidorDeArchivos._cantidad_hilos_ejecutandose += 1

    def _quitar_de_cola_portada_album(self):
        """
        Quita la primera portada album de la cola
        """
        with ConvertidorDeArchivos._lock:
            ConvertidorDeArchivos._cola_convertidor_portadas_album.pop()
            ConvertidorDeArchivos._cantidad_hilos_ejecutandose -= 1
            ConvertidorDeArchivos._portada_album_actual_convirtiendo = 0
            if len(ConvertidorDeArchivos._cola_convertidor_portadas_album) > 0 and \
                    ConvertidorDeArchivos._portada_album_actual_convirtiendo == 0:
                self._crear_hilo_convertir_cancion_personal()

    def _crear_hilo_convertir_portada_creador_de_contenido(self):
        """
        Crea un hilo para convertir una cancion personal
        """
        ConvertidorDeArchivos._executor.submit(self._convertir_portada_creador_de_contenido,
                                               ConvertidorDeArchivos._cola_convertidor_portadas_creador_de_contendio[0])
        ConvertidorDeArchivos._portada_creador_de_contenido_actual_convirtiendo = \
            ConvertidorDeArchivos._cola_convertidor_portadas_creador_de_contendio[0]
        ConvertidorDeArchivos._cantidad_hilos_ejecutandose += 1

    def _quitar_de_cola_portada_creadores_de_contenido(self):
        """
        Quita de la cola creador de contenido
        """
        with ConvertidorDeArchivos._lock:
            ConvertidorDeArchivos._cola_convertidor_portadas_creador_de_contendio.pop()
            ConvertidorDeArchivos._cantidad_hilos_ejecutandose -= 1
            ConvertidorDeArchivos._portada_creador_de_contenido_actual_convirtiendo = 0
            if len(ConvertidorDeArchivos._cola_convertidor_portadas_creador_de_contendio) > 0 and \
                    ConvertidorDeArchivos._portada_creador_de_contenido_actual_convirtiendo == 0:
                self._crear_hilo_convertir_portada_creador_de_contenido()

    def _crear_hilo_convertir_portada_usuario(self):
        """
        Crea un hilo para convertir una portada usuario
        """
        ConvertidorDeArchivos._executor.submit(self._convertir_portada_usuario,
                                               ConvertidorDeArchivos._cola_convertidor_portadas_usuario[0])
        ConvertidorDeArchivos._portada_usuario_actual_convirtiendo = \
            ConvertidorDeArchivos._cola_convertidor_portadas_usuario[0]
        ConvertidorDeArchivos._cantidad_hilos_ejecutandose += 1

    def _quitar_de_cola_portada_usuario(self):
        """
        Quita de la cola la primera portada de la cola usuario
        """
        with ConvertidorDeArchivos._lock:
            ConvertidorDeArchivos._cola_convertidor_portadas_usuario.pop()
            ConvertidorDeArchivos._cantidad_hilos_ejecutandose -= 1
            ConvertidorDeArchivos._portada_usuario_actual_convirtiendo = 0
            if len(ConvertidorDeArchivos._cola_convertidor_portadas_usuario) > 0 and \
                    ConvertidorDeArchivos._portada_usuario_actual_convirtiendo == 0:
                self._crear_hilo_convertir_portada_usuario()
