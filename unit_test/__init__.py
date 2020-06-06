import unittest
from app import create_app, base_de_datos


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

    def tearDown(self):
        """
        Elimina la base de datos cuando se terminan de ejecutar las pruebas
        """
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            base_de_datos.session.remove()
            base_de_datos.drop_all()
