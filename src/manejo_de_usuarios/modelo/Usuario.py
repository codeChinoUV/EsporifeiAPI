"""
    Se encarga de representar a un USUARIO y manejar el acceso del objeto a la base de datos
"""
from flask_sqlalchemy import SQLAlchemy

base_de_datos = SQLAlchemy()


def inicializar_base_de_datos(app):
    """
    Inicializa la clase SQLAlchemy al pasarle como referencia la app Flask que contiene la configuracion de la base de
    datos
    """
    base_de_datos.init_app(app)
    app.app_context().push()


class Usuario(base_de_datos.Model):
    """
    Se encarga de representar el modelo usuario y define su estructura en la base de datos
    """
    nombre_usuario = base_de_datos.Column(base_de_datos.String(20), primary_key=True)
    nombre = base_de_datos.Column(base_de_datos.String(70), nullable=False)
    contrasena = base_de_datos.Column(base_de_datos.String(64), nullable=False)
    tipo_usuario = base_de_datos.Column(base_de_datos.Integer, nullable=False)

    def guardar(self):
        """
        Guarda la informacion del objeto en la base de datos
        :return: None
        """
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    @staticmethod
    def obtener_todos_los_usuario():
        """
        Recupera todos los usuarios registrados en la base de datps
        :return: Una lista con los usuarios en la base de datos
        """
        return Usuario.query.all()

    @staticmethod
    def verificar_nombre_usuario_disponible(nombre_usuario):
        """
        Verifica si el nombre de usuario ya se encuentra en uso
        :param nombre_usuario: El nombre de usuario a verificar
        :return: Verdadero si el nombre de usuario se encuentra disponible o falso si no
        """
        usuarios_con_el_mismo_nombre = Usuario.query.filter_by(nombre_usuario=nombre_usuario).count()
        return not usuarios_con_el_mismo_nombre > 0

    def obtener_json(self):
        """
        Crea un diccionario que representa al objeto a partir de la información del mismo
        :return: Un diccionario con la información del objeto
        """
        json = {'nombre_usuario': self.nombre_usuario, 'nombre': self.nombre}
        return json
