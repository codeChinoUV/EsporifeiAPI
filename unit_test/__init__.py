import unittest
from app import create_app, base_de_datos
from app.administracion_de_contenido.modelo.modelos import Genero, CreadorDeContenido, Album, Cancion, Calificacion
from app.manejo_de_usuarios.modelo.modelos import Usuario


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        """
        Inicializa crea una app y un cliente para poder ser usados en las pruebas
        """
        self.app = create_app(settings_module="config.testing")
        self.client = self.app.test_client()
        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            base_de_datos.create_all()
            BaseTestClass._crear_usuario("creadorDeContenido", "123456", "Creador de contenido", 1,
                                         "creador_de_contenido@exmaple.com")
            BaseTestClass._crear_usuario("consumidorDeMusica", "123456", "Consumidor de musica", 2,
                                         "consumidor_de_musica@example.com")
            BaseTestClass._crear_usuario("creadorDeContenido2", "123456", "Creador de contenido", 1,
                                         "creador_de_contenido2@exmaple.com")
            BaseTestClass._crear_genero("Dance")
            BaseTestClass._crear_genero("Regueton")
            creador_de_contenido = BaseTestClass._crear_creador_de_contenido("prueba1", "Es solo una prueba", True, 1)
            album = BaseTestClass._crear_album("Album de prueba", "2001", 1)
            BaseTestClass._agregar_cancion(album, creador_de_contenido, "cancion de prueba")
            BaseTestClass._agregar_calificacion(1, 1, 3)

    def tearDown(self):
        """
        Elimina la base de datos cuando se terminan de ejecutar las pruebas
        """
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            base_de_datos.session.remove()
            base_de_datos.drop_all()

    @staticmethod
    def _crear_usuario(nombre_usuario, contrasena, nombre, tipo_usuario, correo_electronico):
        """
        Crea un nuevo usuario y lo guarda en la base de datos
        :param nombre_usuario: El nombre_usuario a registrar
        :param nombre: El nombre a registrar
        :param contrasena: La contrasena del usuario
        :param tipo_usuario: El tipo del usuario
        :param correo_electronico: El correo electronico a del usuario
        :return: None
        """
        usuario = Usuario(nombre_usuario=nombre_usuario, contrasena=contrasena, nombre=nombre,
                          tipo_usuario=tipo_usuario, correo_electronico=correo_electronico)
        usuario.guardar()

    @staticmethod
    def _crear_creador_de_contenido(nombre, biografia, es_grupo, id_usuario):
        """
        Crea un nuevo CreadorDeContenido y lo guarda en la base de datos
        :param nombre: El nombre que tendra el creador de contenido
        :param biografia: La biografia del creador de contenido
        :param es_grupo: Indica si el creador de contenido es un grupo
        :param id_usuario: El id del usuario del cual es el creador de contenido
        :return: El creador de contenido realizado
        """
        creador_de_contenido = CreadorDeContenido(nombre=nombre, biografia=biografia, es_grupo=es_grupo,
                                                  usuario_id_usuario=id_usuario)
        creador_de_contenido.guardar()
        return creador_de_contenido

    @staticmethod
    def _crear_genero(nombre_genero):
        """
        Registra un nuevo genero en la base de datos
        :param nombre_genero: El nombre que tendra el genero a registrar
        :return: None
        """
        genero = Genero(genero=nombre_genero)
        base_de_datos.session.add(genero)
        base_de_datos.session.commit()

    @staticmethod
    def _crear_album(nombre, anio_lanzamiento, id_creador_de_contenido):
        """
        Crea un nuevo album y lo guarda en la base de datos
        :param nombre: El nombre del album
        :param anio_lanzamiento: El anio de lanzamiento del album
        :param id_creador_de_contenido: El id del creador de contenido al cual le pertece el album
        :return: El Album creado
        """
        album = Album(nombre=nombre, anio_lanzamiento=anio_lanzamiento, creador_de_contenido_id=id_creador_de_contenido)
        album.guardar()
        return album

    @staticmethod
    def _agregar_cancion(album, creador_de_contenido, nombre_cancion):
        """
        Crea una cancion y la agrega a el album
        :param album: El album en donde se agregara la cancion
        :param creador_de_contenido: El creador_de_contenido que agrego la cancion
        :param nombre_cancion: El nombre que tendra la cancion
        :return: None
        """
        cancion = Cancion(nombre=nombre_cancion)
        album.agregar_cancion(cancion, creador_de_contenido)

    @staticmethod
    def _agregar_calificacion(id_usuario, id_cancion, calificacion):
        """
        Crea una calificacion y la guarda en la base de datos
        :param id_cancion: El id de la calificacion a guardar
        :param id_usuario: El id del usuario que realiza la calificacion
        :return: None
        """
        calificacion = Calificacion(id_usuario=id_usuario, id_cancion=id_cancion, calificacion_estrellas=calificacion)
        calificacion.guardar()
