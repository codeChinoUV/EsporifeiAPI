import unittest

from app import create_app, base_de_datos
from app.manejo_de_usuarios.modelo.modelos import Usuario


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        """
        Crea la base de datos y crea dos usuarios cuando la prueba se ejecuta
        :return:
        """
        self.app = create_app(settings_module="config.testing")
        self.client = self.app.test_client()

        # Crea un contexto de aplicacion
        with self.app.app_context():
            # Crea las tablas de la base de datos
            base_de_datos.create_all()
            BaseTestClass.crear_usuario("creadorDeContenido", "123456", "Creador de contenido", 1)
            BaseTestClass.crear_usuario("consumidorDeMusica", "123456", "Consumidor de musica", 2)

    def tearDown(self):
        """
        Elimina todas las tablas de la base de datos cuando se termina de ejecutar las pruebas
        :return:
        """
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            base_de_datos.session.remove()
            base_de_datos.drop_all()

    @staticmethod
    def crear_usuario(nombre_usuario, contrasena, nombre, tipo_usuario):
        """
        Guarda un nuevo usuario en la base de datos de forma directa
        :param nombre_usuario: El nombre que tendra la cuenta del usuario
        :param contrasena: La constrasena que tendra el usuario
        :param nombre: El nombre del usuario
        :param tipo_usuario: El tipo de usuario
        :return: None
        """
        usuario = Usuario()
        usuario.nombre_usuario = nombre_usuario
        usuario.contrasena = contrasena
        usuario.nombre = nombre
        usuario.tipo_usuario = int(tipo_usuario)
        usuario.guardar()
