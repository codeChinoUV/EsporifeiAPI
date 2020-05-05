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
                                                  nullable=False, index=True)
    eliminado = base_de_datos.Column(base_de_datos.Boolean, nullable=False, default=False)
    artistas = base_de_datos.relationship('Artista', backref='creadordecontenido', lazy=True)

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
        perfiles_con_el_mismo_usuario = CreadorDeContenido.query.filter_by(usuario_nombre_usuario=nombre_usuario,
                                                                           eliminado=False).count()
        return perfiles_con_el_mismo_usuario > 0

    @staticmethod
    def obtener_todos_los_creadores_de_contenido():
        """
        Recupera todos los creadores de contenido registrados en la base de datos
        :return: Una lista con los creadore de contenido registrados
        """
        return CreadorDeContenido.query.filter_by(eliminado=False).all()

    @staticmethod
    def obtener_creador_de_contenido_por_id(id_creador_contenido):
        """
        Recupera el creador de contenido que tenga el id indicado
        :param id_creador_contenido: El id del creador de contenido a recuperar
        :return: El creador de contenido que tiene ese id
        """
        creador_de_contenido = CreadorDeContenido.query.filter_by(id_creador_de_contenido=id_creador_contenido,
                                                                  eliminado=False).first()
        return creador_de_contenido

    @staticmethod
    def obtener_creador_de_contenido_por_usuario(nombre_usuario):
        """
        Recupera el creador de contenido que sea del nombre de usuario
        :param nombre_usuario: El nombre del usuario al que esta asociado el creador de contenido
        :return: El creador de contenido que pertenezca al usuario
        """
        creador_de_contenido = CreadorDeContenido.query.filter_by(usuario_nombre_usuario=nombre_usuario,
                                                                  eliminado=False).first()
        return creador_de_contenido

    @staticmethod
    def obtener_creador_de_contenido_por_busqueda(cadena_busqueda):
        """
        Busca a los creadores de contenido que su nombre contenga la candena de busqueda
        :param cadena_busqueda: La cadena de se utilizara para realizar la busqueda
        :return: Una lista con los creadores que consisten con la cadena de busqueda
        """
        expresion_regular_de_busqueda = "%" + cadena_busqueda + "%"
        creadores_de_contenido = CreadorDeContenido.query. \
            filter(CreadorDeContenido.nombre.ilike(expresion_regular_de_busqueda)).filter_by(eliminado=False).all()
        return creadores_de_contenido

    @staticmethod
    def actualizar_creador_de_contenido():
        """
        Guarda los cambios realizados a un modelo en la base de datos
        """
        base_de_datos.session.commit()

    def eliminar(self):
        """
        Cambia el estado del creador de contenido a eliminado y lo almacena en la base de datos
        :return: none
        """
        self.eliminado = True
        base_de_datos.session.commit()


class Artista(base_de_datos.Model):
    """
    Representa a un artista de un CreadorDeContenido que es grupo
    """
    id_artista = base_de_datos.Column(base_de_datos.Integer, primary_key=True)
    nombre = base_de_datos.Column(base_de_datos.String(70), nullable=False)
    fecha_de_nacimiento = base_de_datos.Column(base_de_datos.Date, nullable=False)
    creador_de_contenido_id = base_de_datos.Column(base_de_datos.Integer,
                                                   base_de_datos.
                                                   ForeignKey('creador_de_contenido.id_creador_de_contenido'),
                                                   nullable=False)

    def obtener_json(self):
        """
        Genera un diccionario con los datos del objeto, el cual se utilizara para serializar la información a un JSON
        :return: Un diccionario con los datos del artista
        """
        diccionario = {'id': self.id_artista,
                       'nombre': self.nombre,
                       'fecha_de_nacimiento': self.fecha_de_nacimiento}
        return diccionario

    @staticmethod
    def obtener_artistas_de_creador_de_contenido(id_creador_de_cotenido):
        """
        Recupera de la base de datos todos artistas que pertenecen al creador de contenido
        :param id_creador_de_cotenido: El id del creador de contenido al que pertencen los artistas
        :return: Los artistas que pertenecen al creador de contenido
        """
        artistas = Artista.query.filter_by(creador_de_contenido_id=id_creador_de_cotenido).all()
        return artistas
