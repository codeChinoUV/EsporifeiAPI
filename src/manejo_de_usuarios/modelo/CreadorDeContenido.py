"""
    Se encarga de representar a un CreadorDeContenido y manejar el acceso del objeto a la base de datos
"""
from flask_sqlalchemy import SQLAlchemy

from src.manejo_de_usuarios.modelo.Usuario import Usuario

base_de_datos = SQLAlchemy()


def inicializar_base_de_datos(app):
    """
    Inicializa la clase SQLAlchemy al pasarle como referencia la app Flask que contiene la configuracion de la base de
    datos
    """
    base_de_datos.init_app(app)
    app.app_context().push()


class CreadorDeContenido(base_de_datos.Model):
    """
    Se encarga de representar el modelo CREADORDECONTENIDO y su acceso a la base de datos
    """
    id_creador_de_contenido = base_de_datos.Column(base_de_datos.Integer, primary_key=True)
    nombre = base_de_datos.Column(base_de_datos.String(70), nullable=False)
    biografia = base_de_datos.Column(base_de_datos.String(500), nullable=True)
    es_grupo = base_de_datos.Column(base_de_datos.Boolean, nullable=False)
    usuario_nombre_usuario = base_de_datos.Column(base_de_datos.String(20),
                                                  base_de_datos.ForeignKey(Usuario.nombre_usuario), nullable=False)

    def guardar(self):
        """
        Guarda en la base de datos los atributos del CreadorDeContenido
        :return:
        """
        base_de_datos.session.add(self)
        base_de_datos.session.commit()
