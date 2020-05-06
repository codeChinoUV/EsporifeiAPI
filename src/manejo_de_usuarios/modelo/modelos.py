"""
    Se encarga de representar a un USUARIO y manejar el acceso del objeto a la base de datos
"""
from src import base_de_datos
from src.manejo_de_usuarios.modelo.enum.enums import TipoUsuario


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
    def verificar_nombre_usuario_en_uso(nombre_usuario):
        """
        Verifica si el nombre de usuario ya se encuentra en uso
        :return: Verdadero si el nombre de usuario se encuentra disponible o falso si no
        """
        usuarios_con_el_mismo_nombre = Usuario.query.filter_by(nombre_usuario=nombre_usuario).count()
        return usuarios_con_el_mismo_nombre > 0

    def obtener_json(self):
        """
        Crea un diccionario que representa al objeto a partir de la información del mismo
        :return: Un diccionario con la información del objeto
        """
        json = {'nombre_usuario': self.nombre_usuario, 'nombre': self.nombre, 'tipo_usuario': self.tipo_usuario}
        return json

    @staticmethod
    def validar_usuario_creador_de_contenido(nombre_usuario):
        """
        Valida que el usuario sea de tipo creador de contenido
        :return: Verdadero si el usuario es creador de contenido o falso si no
        """
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        return TipoUsuario(usuario.tipo_usuario) == TipoUsuario.CreadorDeContenido

    @staticmethod
    def validar_credenciales(nombre_usuario, contrasena):
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario, contrasena=contrasena).first()
        return usuario
