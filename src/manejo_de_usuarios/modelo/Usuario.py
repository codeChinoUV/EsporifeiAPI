""""
    Se encarga de representar a un USUARIO y manejar el acceso del objeto a la base de datos
"""
from flask_sqlalchemy import SQLAlchemy

base_de_datos = SQLAlchemy()


def inicializar_base_de_datos(app):
    base_de_datos.init_app(app)


class Usuario(base_de_datos.Model):
    nombre_usuario = base_de_datos.Column(base_de_datos.String(50), primary_key=True)
    nombre = base_de_datos.Column(base_de_datos.String(70), nullable=False)
    contrasena = base_de_datos.Column(base_de_datos.String(64), nullable=False)
    tipo_usuario = base_de_datos.Column(base_de_datos.Integer, nullable=False)

    def guardar(self):
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    @staticmethod
    def obtener_todos_los_usuario():
        return Usuario.query.all()

    def obtener_json(self):
        json = {}
        json['nombre_usuario'] = self.nombre_usuario
        json['nombre'] = self.nombre
        json['contrasena'] = self.contrasena
        return json
