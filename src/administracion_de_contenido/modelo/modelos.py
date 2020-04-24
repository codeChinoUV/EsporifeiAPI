"""
    Se encarga de representar a un CreadorDeContenido y manejar el acceso del objeto a la base de datos
"""
from src import base_de_datos


class CreadorDeContenido(base_de_datos.Model):
    """
    Se encarga de representar el modelo CREADORDECONTENIDO y su acceso a la base de datos
    """
    id_creador_de_contenido = base_de_datos.Column(base_de_datos.Integer, primary_key=True)
    nombre = base_de_datos.Column(base_de_datos.String(70), nullable=False)
    biografia = base_de_datos.Column(base_de_datos.String(500), nullable=True)
    es_grupo = base_de_datos.Column(base_de_datos.Boolean, nullable=False)
    usuario_nombre_usuario = base_de_datos.Column(base_de_datos.String(20),
                                                  nullable=False, index=True, unique=True)

    def guardar(self):
        """
        Guarda en la base de datos los atributos del CreadorDeContenido
        :return:
        """
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def obtener_json(self):
        """
        Crea un diccionario con los datos de la clase para poder devolverse como un json
        :return: Un diccionario con los datos de los atributos
        """
        json = {'id': self.id_creador_de_contenido, 'nombre': self.nombre, 'biografia': self.biografia,
                'es_grupo': self.es_grupo}
        return json

    @staticmethod
    def verificar_usuario_ya_tiene_perfil(nombre_usuario):
        """
        Verifica si el nombre de usuario ya tiene un perfil registrado
        :param nombre_usuario: El nombre del usuario a verificar
        :return: Verdadero si el nombre de usuario ya tiene un perfil registrado, falso si no
        """
        perfiles_con_el_mismo_usuario = CreadorDeContenido.query.filter_by(usuario_nombre_usuario=nombre_usuario) \
            .count()
        return perfiles_con_el_mismo_usuario > 0