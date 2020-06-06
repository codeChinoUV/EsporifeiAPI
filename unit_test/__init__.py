import unittest
from app import create_app, base_de_datos
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
