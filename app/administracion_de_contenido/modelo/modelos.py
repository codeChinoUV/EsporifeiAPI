"""
    Se encarga de representar a un CreadorDeContenido y manejar el acceso del objeto a la base de datos
"""
from app import base_de_datos
from app.util.JsonBool import JsonBool

artistas_generos = base_de_datos.Table('artistas_generos',
                                       base_de_datos.Column('id_creador_de_contenido', base_de_datos.Integer,
                                                            base_de_datos.ForeignKey(
                                                                'creador_de_contenido.id_creador_de_contenido'),
                                                            primary_key=True),
                                       base_de_datos.Column('id_genero', base_de_datos.Integer,
                                                            base_de_datos.ForeignKey('genero.id_genero'),
                                                            primary_key=True)
                                       )


class CreadorDeContenido(base_de_datos.Model):
    """
    Se encarga de representar el modelo CreadorDeContenido y su acceso a la base de datos
    """
    id_creador_de_contenido = base_de_datos.Column(base_de_datos.Integer, primary_key=True)
    nombre = base_de_datos.Column(base_de_datos.String(70), nullable=False)
    biografia = base_de_datos.Column(base_de_datos.String(500), nullable=True)
    es_grupo = base_de_datos.Column(base_de_datos.Boolean, nullable=False)
    usuario_id_usuario = base_de_datos.Column(base_de_datos.Integer, nullable=False, index=True)
    generos = base_de_datos.relationship('Genero', secondary=artistas_generos, lazy='subquery',
                                         backref=base_de_datos.backref('genero', lazy=True))

    def guardar(self):
        """
        Guarda en la base de datos los atributos del CreadorDeContenido
        :return:
        """
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def actualizar_informacion(self, nombre, biografia, es_grupo):
        """
        Actauliza la informacion de los atributos de nombre, biografia y es_grupo en la base de datos
        :param nombre: El nombre a actualizar
        :param biografia: La biografia a actualizar
        :param es_grupo: El es_grupo a actualizar
        """
        if nombre is not None:
            self.nombre = nombre
        if biografia is not None:
            self.biografia = biografia
        if es_grupo is not None:
            self.es_grupo = JsonBool.obtener_boolean_de_valor_json(es_grupo)

        base_de_datos.session.commit()

    def obtener_json(self):
        """
        Crea un diccionario con los datos de la clase para poder devolverse como un json
        :return: Un diccionario con los datos de los atributos
        """
        generos = []
        for genero in self.generos:
            generos.append(genero)
        json = {'id': self.id_creador_de_contenido, 'nombre': self.nombre, 'biografia': self.biografia,
                'generos': generos, 'es_grupo': self.es_grupo}
        return json

    @staticmethod
    def verificar_usuario_tiene_creador_contenido_registrado(nombre_usuario):
        """
        Verifica si el nombre de usuario ya tiene un creador de contenido asociado
        :param nombre_usuario: El nombre del usuario a verificar
        :return: Verdadero si el nombre de usuario ya tiene un creador de contenido registrado, falso si no
        """
        perfiles_con_el_mismo_usuario = CreadorDeContenido.query. \
            filter_by(usuario_nombre_usuario=nombre_usuario).count()
        return perfiles_con_el_mismo_usuario > 0

    @staticmethod
    def verificar_existe_creador_contenido(id_creador_contenido):
        """
        Verifica si id_creador_cotenido pertence a un creador de contenido
        :param id_creador_contenido: El id del CreadorDeContenido a validar si existe
        :return: Verdadero si el id_creador_cotenido es de un CreadorDeContenido o falso si no
        """
        cantidad_creadores_contenido_con_mismo_id = \
            CreadorDeContenido.query.filter_by(id_creador_de_contenido=id_creador_contenido).count()
        return cantidad_creadores_contenido_con_mismo_id > 0

    @staticmethod
    def obtener_creador_de_contenido_por_id(id_creador_contenido):
        """
        Recupera el creador de contenido que tenga el id indicado
        :param id_creador_contenido: El id del creador de contenido a recuperar
        :return: El creador de contenido que tiene ese id
        """
        creador_de_contenido = CreadorDeContenido.query.filter_by(id_creador_de_contenido=id_creador_contenido).first()
        return creador_de_contenido

    @staticmethod
    def obtener_creador_de_contenido_por_id_usuario(id_usuario):
        """
        Recupera el creador de contenido que sea del nombre de usuario
        :param id_usuario: El id del usuario al cual pertence el creador de contenido
        :return: El creador de contenido que pertenezca al usuario
        """
        creador_de_contenido = CreadorDeContenido.query.filter_by(usuario_id_usuario=id_usuario).first()
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
            filter(CreadorDeContenido.nombre.ilike(expresion_regular_de_busqueda)).all()
        return creadores_de_contenido


class Genero(base_de_datos.Model):
    """
    Representa a un Genero que agrupa canciones y creadores de contenido
    """
    id_genero = base_de_datos.Column(base_de_datos.Integer, primary_key=True, autoincrement=True)
    genero = base_de_datos.Column(base_de_datos.String(30), nullable=False)
    creadores_de_contenido = base_de_datos.relationship('CreadorDeContenido', secondary=artistas_generos,
                                                        lazy='subquery',
                                                        backref=base_de_datos.backref('creador_de_contenido',
                                                                                      lazy=True))

    @staticmethod
    def recuperar_todos_los_generos():
        """
        Recupera de la base de datos todos los generos registrados
        :return: Una lista con los generos registrados
        """
        generos = Genero.query.all()
        return generos

    def obtener_json(self):
        """
        Crea un diccionario con los atributos del objeto
        :return: Un diccionario con los atributos del objeto
        """
        diccionario_de_los_atributos = {'id': self.id_genero, 'genero': self.genero}
        return diccionario_de_los_atributos


class Disquera(base_de_datos.Model):
    """
    Se encarga de representar una Disquera a la que pertenece un artista
    """
    id_disquera = base_de_datos.Column(base_de_datos.Integer, primary_key=True, autoincrement=True)
    nombre = base_de_datos.Column(base_de_datos.String(70), nullable=False)
    direccion = base_de_datos.Column(base_de_datos.String(200), nullable=False)
    email = base_de_datos.Column(base_de_datos.String(100), nullable=False)
    telefono = base_de_datos.Column(base_de_datos.String(30), nullable=True)
    es_empresa = base_de_datos.Column(base_de_datos.Boolean, nullable=False)
    nombre_usuario_creador = base_de_datos.Column(base_de_datos.String(20), nullable=False)

    def guardar(self):
        """
        Se encarga de guardar el objeto actual en la base de datos
        """
        if self.es_empresa is None:
            self.es_empresa = False
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def obtner_json(self):
        """
        Crea un diccionario con los atributos del objeto
        :return: Un diccionario con los atributos del objeto
        """
        diccionario_de_los_atributos = {'id': self.id_disquera, 'nombre': self.nombre, 'direccion': self.direccion,
                                        'email': self.email, 'telefono': self.telefono, 'es_empresa': self.es_empresa}
        return diccionario_de_los_atributos
