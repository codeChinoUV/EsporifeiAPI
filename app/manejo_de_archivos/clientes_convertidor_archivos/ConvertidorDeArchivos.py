import threading
from concurrent.futures.thread import ThreadPoolExecutor

from app.manejo_de_archivos.manejador_de_archivos.ManejadorCanciones import ManejadorCanciones


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
        pass

    def agregar_portada_creador_de_contenido_a_cola(self, id_creador_de_contenido):
        pass

    def agregar_porada_usuario_a_cola(self, id_usuario):
        pass

    def agregar_cancion_a_cola(self, id_cancion):
        if id_cancion not in ConvertidorDeArchivos._cola_convertidor_canciones:
            ConvertidorDeArchivos._cola_convertidor_canciones.append(id_cancion)
            if ConvertidorDeArchivos._cantidad_hilos_ejecutandose < 5:
                if ConvertidorDeArchivos._cancion_actual_convirtiendo != id_cancion:
                    self._crear_hilo_convertir_cancion()

    def agregar_cancion_personal_a_cola(self, id_cancion_personal):
        pass

    def convertir_cancion(self, id_cancion):
        ManejadorCanciones.convertir_cancion_mp3_todas_calidades(id_cancion)
        self._quitar_de_cola_canciones(id_cancion)

    def _quitar_de_cola_canciones(self, id_cancion):
        with ConvertidorDeArchivos._lock:
            ConvertidorDeArchivos._cola_convertidor_canciones.remove(id_cancion)
            ConvertidorDeArchivos._cantidad_hilos_ejecutandose -= 1
            ConvertidorDeArchivos._cancion_actual_convirtiendo = 0
        if len(ConvertidorDeArchivos._cola_convertidor_canciones) > 0:
            self._crear_hilo_convertir_cancion()

    def _crear_hilo_convertir_cancion(self):
        ConvertidorDeArchivos._executor.submit(self.convertir_cancion,
                                               args=ConvertidorDeArchivos._cola_convertidor_canciones[0])
        ConvertidorDeArchivos._cancion_actual_convirtiendo = ConvertidorDeArchivos._cola_convertidor_canciones[0]
        ConvertidorDeArchivos._cantidad_hilos_ejecutandose += 1
