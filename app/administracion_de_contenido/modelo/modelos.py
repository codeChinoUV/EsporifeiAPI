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

creadores_de_contenido_de_la_cancion = base_de_datos.Table('creadores_canciones',
                                                           base_de_datos.Column('id_creador_de_contenido',
                                                                                base_de_datos.Integer,
                                                                                base_de_datos.ForeignKey(
                                                                                    'creador_de_contenido'
                                                                                    '.id_creador_de_contenido'),
                                                                                primary_key=True),
                                                           base_de_datos.Column('id_cancion', base_de_datos.Integer,
                                                                                base_de_datos.ForeignKey(
                                                                                    'cancion.id_cancion'),
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
                                         backref=base_de_datos.backref('creadores_de_contenido', lazy=True))

    def guardar(self):
        """
        Guarda en la base de datos los atributos del CreadorDeContenido
        :return:
        """
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def editar(self, nombre, biografia, es_grupo):
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
            generos.append(genero.obtener_json())
        json = {'id': self.id_creador_de_contenido, 'nombre': self.nombre, 'biografia': self.biografia,
                'generos': generos, 'es_grupo': self.es_grupo}
        return json

    def obtener_json_sin_genero(self):
        """
        Crea un diccionario con los datos del objeto omitiendo los generos para poder devolverse como un json
        :return: Un diccionario con los datos de los atributos
        """
        generos = []
        json = {'id': self.id_creador_de_contenido, 'nombre': self.nombre, 'biografia': self.biografia,
                'generos': generos, 'es_grupo': self.es_grupo}
        return json

    @staticmethod
    def verificar_usuario_tiene_creador_contenido_registrado(id_usuario):
        """
        Verifica si el nombre de usuario ya tiene un creador de contenido asociado
        :param id_usuario: El id del usuario a verificar
        :return: Verdadero si el nombre de usuario ya tiene un creador de contenido registrado, falso si no
        """
        perfiles_con_el_mismo_usuario = CreadorDeContenido.query. \
            filter_by(usuario_id_usuario=id_usuario).count()
        return perfiles_con_el_mismo_usuario > 0

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
    def obtener_creador_de_contenido_por_busqueda(cadena_busqueda, cantidad=10, pagina=1):
        """
        Busca a los creadores de contenido que su nombre contenga la candena de busqueda
        :param cadena_busqueda: La cadena de se utilizara para realizar la busqueda
        :param cantidad: La cantidad de elementos a recuperar por pagina, el valor por defecto es 10
        :param pagina: El numero de pagina el cual se desea recuperar, el valor por defecto es 1
        :return: Una lista con los creadores que consisten con la cadena de busqueda
        """
        expresion_regular_de_busqueda = "%" + cadena_busqueda + "%"
        cantidad_total = cantidad * pagina
        creadores_de_contenido = CreadorDeContenido.query. \
            filter(CreadorDeContenido.nombre.ilike(expresion_regular_de_busqueda)).limit(cantidad_total).all()
        if len(creadores_de_contenido) > (cantidad * (pagina - 1)):
            creadores_de_cotenido_pagina = []
            for i in range(cantidad):
                posicion = i + (cantidad * (pagina - 1))
                try:
                    creadores_de_cotenido_pagina.append(creadores_de_contenido[posicion])
                except IndexError:
                    break
            return creadores_de_cotenido_pagina
        else:
            creadores_de_contenido = []
            return creadores_de_contenido

    @staticmethod
    def verificar_existe_creador_contenido(id_creador_contenido):
        """
        Verifica si id_creador_contenido pertenece a un creador de contenido
        :param id_creador_contenido: El id del CreadorDeContenido a validar si existe
        :return: Verdadero si el id_creador_cotenido es de un CreadorDeContenido o falso si no
        """
        cantidad_creadores_contenido_con_mismo_id = \
            CreadorDeContenido.query.filter_by(id_creador_de_contenido=id_creador_contenido).count()
        return cantidad_creadores_contenido_con_mismo_id > 0

    def validar_tiene_genero(self, id_genero):
        """
        Valida si el creador de contenido tiene el genero con el id_genero
        :param id_genero: El id del genero a buscar
        :return: True si lo tiene o False si no
        """
        tiene_genero = False
        for genero in self.generos:
            if genero.id_genero == id_genero:
                tiene_genero = True
                break
        return tiene_genero


generos_de_la_cancion = base_de_datos.Table('generos_de_la_cancion',
                                            base_de_datos.Column('id_cancion', base_de_datos.Integer,
                                                                 base_de_datos.ForeignKey(
                                                                     'cancion.id_cancion'),
                                                                 primary_key=True),
                                            base_de_datos.Column('id_genero', base_de_datos.Integer,
                                                                 base_de_datos.ForeignKey('genero.id_genero'),
                                                                 primary_key=True)
                                            )


class Genero(base_de_datos.Model):
    """
    Representa a un Genero que agrupa canciones y creadores de contenido
    """
    id_genero = base_de_datos.Column(base_de_datos.Integer, primary_key=True, autoincrement=True)
    genero = base_de_datos.Column(base_de_datos.String(30), nullable=False)

    @staticmethod
    def recuperar_todos_los_generos():
        """
        Recupera de la base de datos todos los generos registrados
        :return: Una lista con los generos registrados
        """
        generos = Genero.query.all()
        return generos

    @staticmethod
    def obtener_genero_por_id(id_genero):
        """
        Recupera el genero que tiene el id_genero
        :param id_genero: El id del genero a recuperar
        :return: Un genero o None si el genero no existe
        """
        genero = Genero.query.filter_by(id_genero=id_genero).first()
        return genero

    def obtener_json(self):
        """
        Crea un diccionario con los atributos del objeto
        :return: Un diccionario con los atributos del objeto
        """
        diccionario_de_los_atributos = {'id': self.id_genero, 'genero': self.genero}
        return diccionario_de_los_atributos

    def agregar_creador_de_contenido(self, creador_de_contenido):
        """
        Agrega un creador_de_contenido a la lista de creadores de contenido
        :param creador_de_contenido: El creador de contenido a agregar
        :return: None
        """
        self.creadores_de_contenido.append(creador_de_contenido)
        base_de_datos.session.commit()

    def eliminar_creador_de_contenido(self, creador_de_contenido):
        """
        Elimina a un creador de contenido del genero
        :param creador_de_contenido: El creador de contenido a eliminar
        :return: None
        """
        self.creadores_de_contenido.remove(creador_de_contenido)
        base_de_datos.session.commit()


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


albumes_de_la_cancion = base_de_datos.Table('albumes_de_la_cancion',
                                            base_de_datos.Column('id_album', base_de_datos.Integer,
                                                                 base_de_datos.ForeignKey(
                                                                     'album.id_album'),
                                                                 primary_key=True),
                                            base_de_datos.Column('id_cancion', base_de_datos.Integer,
                                                                 base_de_datos.ForeignKey('cancion.id_cancion'),
                                                                 primary_key=True)
                                            )


class Album(base_de_datos.Model):
    id_album = base_de_datos.Column(base_de_datos.Integer, primary_key=True)
    nombre = base_de_datos.Column(base_de_datos.String(70), nullable=False)
    anio_lanzamiento = base_de_datos.Column(base_de_datos.String(4), nullable=False)
    duracion_total_segundos = base_de_datos.Column(base_de_datos.Float)
    eliminado = base_de_datos.Column(base_de_datos.Boolean, nullable=False, default=False)
    creador_de_contenido_id = base_de_datos.Column(base_de_datos.Integer,
                                                   base_de_datos.
                                                   ForeignKey('creador_de_contenido.id_creador_de_contenido'),
                                                   nullable=False)
    canciones = base_de_datos.relationship('Cancion', secondary=albumes_de_la_cancion, lazy='subquery',
                                           backref=base_de_datos.backref('albumes', lazy=True))

    def guardar(self):
        """
        Se encarga de guardar el objeto actual en la base de datos
        """
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def actualizar_informacion(self, nombre, anio_lanzamiento):
        """
        Actualiza la informacion del nombre del objeto y lo guarda en la base de datos
        :param nombre: El nombre actualizado
        :param anio_lanzamiento: El año de lanzamiento actualizado
        """
        self.nombre = nombre
        self.anio_lanzamiento = anio_lanzamiento
        base_de_datos.session.commit()

    def eliminar_informacion(self):
        """
        Actualiza la informacion del valor eliminado del objeto y lo guarda en la base de datos
        :return: None
        """
        self.eliminado = True
        base_de_datos.session.commit()

    @staticmethod
    def obtener_abumes_creador_de_contenido(id_creador_de_contenido):
        """
        Obtener un listado de álbumes pertenecientes a un
        creador de contenido
        :param id_creador_de_contenido: El id del creador de contenido que es dueño del álbum
        :return: Una lista de álbumes o una lista vacía
        """
        albumes = Album.query.filter_by(creador_de_contenido_id=id_creador_de_contenido, eliminado=False).all()
        if albumes is None:
            return []
        return albumes

    @staticmethod
    def obtener_album_por_id(id_album):
        """
        Recupera de la base de datos el álbum que tiene el id_album
        :param id_album: El id del álbum a recuperar
        :return: El álbum que coincide con el id_album o None si ningún álbum tiene el id_album
        """
        album = Album.query.filter_by(id_album=id_album, eliminado=False).first()
        return album

    @staticmethod
    def verificar_album_existe(id_album):
        """
        Verifica si un álbum existe en la base de datos
        :param id_album: El id del álbum a verificar si existe
        :return: Verdadero si el álbum existe, falso si no
        """
        cantidad_de_albumes_con_el_id = Album.query.filter_by(id_album=id_album).count()
        return cantidad_de_albumes_con_el_id > 0

    @staticmethod
    def obtener_album_por_busqueda(cadena_busqueda):
        """
        Busca los álbumes cuyo nombre contenga la cadena de búsqueda
        :param cadena_busqueda: La cadena que se utilizará para realizar la búsqueda
        :return: Una lista con los álbumes que coinciden con la cadena de búsqueda
        """
        expresion_regular_de_busqueda = "%" + cadena_busqueda + "%"
        albumes = Album.query. \
            filter(Album.nombre.ilike(expresion_regular_de_busqueda)).all()
        return albumes

    @staticmethod
    def validar_pertenece_album(id_creador_de_contenido, id_album):
        """
        Valida si el album es dueño del creador de contenido
        :param id_album: El id del album a verificar el dueño
        :param id_creador_de_contenido: El creador de contenido a validar si es dueño
        :return: Verdadero si el creador de contenido es dueño o falso si no
        """
        cantidad_de_albumes = Album.query \
            .filter_by(id_album=id_album, creador_de_contenido_id=id_creador_de_contenido).count()
        return cantidad_de_albumes > 0

    def obtener_json(self):
        """
        Crea un diccionario con los atributos del objeto
        :return: Un diccionario con los atributos del objeto
        """
        diccionario_del_objeto = {'id': self.id_album, 'nombre': self.nombre, 'anio_lanzamiento': self.anio_lanzamiento,
                                  'duracion_total': self.duracion_total_segundos}
        return diccionario_del_objeto

    def agregar_cancion(self, cancion, creador_de_contenido):
        """
        Agrega una cancion al album y agrega el creador_de_contenido a la cancion y la guarda en la base de datos
        :param cancion: La cancion a agregar al album
        :param creador_de_contenido: El creador de contenido a agregar a la cancion
        :return: None
        """
        self.canciones.append(cancion)
        cancion.creadores_de_contenido.append(creador_de_contenido)
        base_de_datos.session.commit()


canciones_de_listas_reproduccion = base_de_datos.Table('canciones_de_listas_reproduccion',
                                                       base_de_datos.Column('id_lista_de_reproduccion',
                                                                            base_de_datos.Integer,
                                                                            base_de_datos.ForeignKey(
                                                                                'lista_de_reproduccion'
                                                                                '.id_lista_de_reproduccion'),
                                                                            primary_key=True),
                                                       base_de_datos.Column('id_cancion', base_de_datos.Integer,
                                                                            base_de_datos.ForeignKey(
                                                                                'cancion.id_cancion'),
                                                                            primary_key=True)
                                                       )


class Cancion(base_de_datos.Model):
    id_cancion = base_de_datos.Column(base_de_datos.Integer, primary_key=True)
    nombre = base_de_datos.Column(base_de_datos.String(70), nullable=False)
    duracion_en_segundos = base_de_datos.Column(base_de_datos.Float, default=0)
    cantidad_de_reproducciones = base_de_datos.Column(base_de_datos.Integer, default=0)
    calificacion_promedio = base_de_datos.Column(base_de_datos.Float, default=0)
    eliminada = base_de_datos.Column(base_de_datos.Boolean, default=False)
    creadores_de_contenido = base_de_datos.relationship('CreadorDeContenido',
                                                        secondary=creadores_de_contenido_de_la_cancion, lazy='subquery',
                                                        backref=base_de_datos.backref('creadores_de_contenido',
                                                                                      lazy=True))
    generos = base_de_datos.relationship('Genero',
                                         secondary=generos_de_la_cancion, lazy='subquery',
                                         backref=base_de_datos.backref('generos', lazy=True))

    def obtener_json_con_creadores(self):
        """
        Crea un diccionario con la informacion de las cancion, incluyendo la informacion de los creadores de contenido
        :return: Un diccionario
        """
        creadores_de_contenido = []
        for creador_de_contenido in self.creadores_de_contenido:
            creadores_de_contenido.append(creador_de_contenido.obtener_json_sin_genero())
        diccionario = {'id: ': self.id_cancion, 'nombre': self.nombre,
                       'duracion': self.duracion_en_segundos,
                       'cantidad_de_reproducciones': self.cantidad_de_reproducciones,
                       'creadores_de_contenido': creadores_de_contenido,
                       'calificacion_promedio': self.calificacion_promedio,
                       'album': None}
        return diccionario

    def obtener_json_con_album(self):
        """
        Crea un diccionario con la informacion de las cancion, incluyendo la informacion de los creadores de contenido y
        del album al que pertenece
        :return: Un diccionario
        """
        album = self.albumes[0]
        diccionario = self.obtener_json_con_creadores()
        diccionario['album'] = album.obtener_json()
        return diccionario

    def agregar_creador_de_contenido(self, creador_de_contenido):
        """
        Agrega un creador_de_contenido a la cancion
        :param creador_de_contenido: El creador de contenido a agregar
        :return: None
        """
        self.creadores_de_contenido.append(creador_de_contenido)
        base_de_datos.session.commit()

    def eliminar_creador_de_contenido(self, creador_de_contenido):
        """
        Elimina al creador de contenido de la lista de creadores de contenido
        :param creador_de_contenido: El creador de contenido a quitar
        :return: None
        """
        if creador_de_contenido != self.creadores_de_contenido[0]:
            self.creadores_de_contenido.remove(creador_de_contenido)
            base_de_datos.session.commit()

    def actualizar_calificacion_promedio(self, nueva_calificacion):
        """
        Actualiza la calificacion promedio de la cancion
        :param nueva_calificacion: La nueva calificacion promedio que tendra la cancion
        :return: None
        """
        self.calificacion_promedio = nueva_calificacion
        base_de_datos.session.commit()

    @staticmethod
    def obtener_cancion_por_id(id_cancion):
        """
        Recupera la cancion que tiene el id_cancion
        :param id_cancion: El id de la cancion a recuperar
        :return: La cancion que tiene el id_cancion o None si no existe la cancion con ese id
        """
        cancion = Cancion.query.filter_by(id_cancion=id_cancion, eliminada=False).first()
        return cancion

    @staticmethod
    def validar_existe_cancion_en_album(id_album, id_cancion):
        """
        Valida si el id de la cancion pertenece a la cancion
        :param id_album: El id del album en donde se buscara la cancion
        :param id_cancion: El id de la cancion a validar si existe
        :return: Verdadero si existe una cancion con el id o Falso si no
        """
        se_encuentra_en_album = False
        album = Album.obtener_album_por_id(id_album)
        for cancion in album.canciones:
            if cancion.id_cancion == id_cancion:
                se_encuentra_en_album = True
                break
        return se_encuentra_en_album

    def editar(self, nombre):
        """
        Actualiza la informaciòn del nombre de la cancion
        :param nombre: El nombre que se le asignara a la cancion
        :return: None
        """
        self.nombre = nombre
        base_de_datos.session.commit()

    def eliminar(self):
        """
        Cambia el estado de eliminado a la cancion
        :return: None
        """
        self.eliminada = True
        base_de_datos.session.commit()

    def agregar_genero(self, genero):
        """
        Agrega un genero a la lista de generos de la cancion
        :param genero: El genero a agregar
        :return: None
        """
        self.generos.append(genero)
        base_de_datos.session.commit()

    def eliminar_genero(self, genero):
        """
        Elimina un genero de la lista de generos de la cancion
        :param genero: El genero a eliminar
        :return: None
        """
        self.generos.remove(genero)
        base_de_datos.session.commit()

    def validar_tiene_genero(self, id_genero):
        """
        Valida si la cancion tiene un genero con el id_genero
        :param id_genero: El id del genero a validar
        :return: Verdadero si tiene el genero o Falso si no
        """
        tiene_genero = False
        for genero in self.generos:
            if genero.id_genero == id_genero:
                tiene_genero = True
                break
        return tiene_genero

    @staticmethod
    def obtener_canciones_por_busqueda(cadena_busqueda, cantidad=10, pagina=1):
        """
        Busca a las canciones que su nombre contenga la candena de busqueda
        :param cadena_busqueda: La cadena de busqueda que se utilizara para realizar la busqueda
        :param cantidad: La cantidad de elementos a recuperar por pagina, el valor por defecto es 10
        :param pagina: El numero de pagina el cual se desea recuperar, el valor por defecto es 1
        :return: Una lista con las canciones que coinciden con la cadena de busqueda
        """
        expresion_regular_de_busqueda = "%" + cadena_busqueda + "%"
        cantidad_total = cantidad * pagina
        canciones = Cancion.query. \
            filter(Cancion.nombre.ilike(expresion_regular_de_busqueda)).order_by(Cancion.cantidad_de_reproducciones) \
            .limit(cantidad_total).all()
        if len(canciones) > (cantidad * (pagina - 1)):
            canciones_de_la_pagina = []
            for i in range(cantidad):
                posicion = i + (cantidad * (pagina - 1))
                try:
                    canciones_de_la_pagina.append(canciones[posicion])
                except IndexError:
                    break
            return canciones_de_la_pagina
        else:
            canciones = []
            return canciones

    def validar_cancion_tiene_creador_de_contenido(self, id_creador_de_contenido):
        """
        Se encarga de validar si la cancion tiene el creador de contenido
        :param id_creador_de_contenido: El id del creador de contenido a validar si lo tiene
        :return: True si la cancion tiene al creador de contenido o False si no
        """
        tiene_creador = False
        for creador in self.creadores_de_contenido:
            if creador.id_creador_de_contenido == id_creador_de_contenido:
                tiene_creador = True
                break
        return tiene_creador


class Calificacion(base_de_datos.Model):
    id_usuario = base_de_datos.Column(base_de_datos.Integer, base_de_datos.ForeignKey('usuario.id_usuario'),
                                      nullable=False, primary_key=True)
    id_cancion = base_de_datos.Column(base_de_datos.Integer, base_de_datos.ForeignKey('cancion.id_cancion'),
                                      nullable=False, primary_key=True)
    calificacion_estrellas = base_de_datos.Column(base_de_datos.Integer, nullable=False)

    def guardar(self):
        """
        Guarda el objeto actual y actualiza la calificacion promedio de la cancion
        """
        Calificacion._actualizar_nueva_calificacion_promedio_cancion(self.id_cancion, self.calificacion_estrellas)
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def eliminar(self):
        """
        Elimina la calificacion actual y actualiza la calificacion promedio de la cancion
        :return: None
        """
        Calificacion._actualizar_quitar_calificacion_promedio_cancion(self.id_cancion, self.calificacion_estrellas)
        base_de_datos.session.delete(self)
        base_de_datos.session.commit()

    def editar_calificacion(self, calificacion):
        """
        Edita la calificacion actual y actualiza la calificacion promedio de la cancion
        :param calificacion: La nueva calificacion
        :return: None
        """
        Calificacion._actualizar_editar_calificacion_promedio_cancion(self.id_cancion, self.calificacion_estrellas,
                                                                      calificacion)
        self.calificacion_estrellas = calificacion
        base_de_datos.session.commit()

    @staticmethod
    def obtener_calificacion(id_cancion, id_usuario):
        """
        Recupera la calificacion que tenga el id_cancion y el id_usuario
        :param id_cancion: El id de la cancion que calificada
        :param id_usuario: El id del usuario que califica a la cancion
        :return: Una Calificacion
        """
        calificacion = Calificacion.query.filter_by(id_usuario=id_usuario, id_cancion=id_cancion).first()
        return calificacion

    @staticmethod
    def _actualizar_quitar_calificacion_promedio_cancion(id_cancion, calificacion):
        """
        Calcula la nueva calificacion promedio y se la actualiza a la cancion
        :param calificacion: La calificacion quitada
        :return: None
        """
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        cantidad_calificaciones = Calificacion._obtener_cantidad_de_calificaciones(id_cancion)
        total_calificacion = (cantidad_calificaciones * cancion.calificacion_promedio) - int(calificacion)
        cantidad_calificaciones = (cantidad_calificaciones - 1)
        if cantidad_calificaciones == 0:
            nuevo_promedio = 0
        else:
            nuevo_promedio = total_calificacion / (cantidad_calificaciones - 1)
        cancion.actualizar_calificacion_promedio(nuevo_promedio)

    @staticmethod
    def _actualizar_editar_calificacion_promedio_cancion(id_cancion, calificacion_antigua, calificacion_nueva):
        """
        Calcula la nueva calificacion promedio y se la actualiza a la cancion
        :param id_cancion: El id de la cancion a modificar el promedio de la calificacion
        :param calificacion_antigua: La calificacion que tenia antes
        :param calificacion_nueva: La nueva calificacion
        :return: None
        """
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        cantidad_calificaciones = Calificacion._obtener_cantidad_de_calificaciones(id_cancion)
        total_calificacion = (cantidad_calificaciones * cancion.calificacion_promedio) - int(calificacion_antigua)
        nuevo_promedio = (total_calificacion + int(calificacion_nueva)) / cantidad_calificaciones
        cancion.actualizar_calificacion_promedio(nuevo_promedio)

    @staticmethod
    def _actualizar_nueva_calificacion_promedio_cancion(id_cancion, nueva_calificacion):
        """
        Calcula la nueva calificacion promedio y se la actualiza a la cancion
        :param nueva_calificacion: La calificacion agregada
        :return: None
        """
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        cantidad_calificaciones = Calificacion._obtener_cantidad_de_calificaciones(id_cancion)
        total_calificacion = (cantidad_calificaciones * cancion.calificacion_promedio) + int(nueva_calificacion)
        nuevo_promedio = total_calificacion / (cantidad_calificaciones + 1)
        cancion.actualizar_calificacion_promedio(nuevo_promedio)

    @staticmethod
    def _obtener_cantidad_de_calificaciones(id_cancion):
        """
        Obtiene el total de calificaciones de una cancion
        :param id_cancion: La cancion la cual se le contara la cantidad de calificaciones que tiene
        :return: La cantidad de calificaciones de la cancion
        """
        cantidad_calificaciones = Calificacion.query.filter_by(id_cancion=id_cancion).count()
        return cantidad_calificaciones

    def obtener_json(self):
        """
        Crea un diccionario con los atributos del modelo
        """
        diccionario = {'calificacion_estrellas': self.calificacion_estrellas}
        return diccionario


class ListaDeReproduccion(base_de_datos.Model):
    id_lista_de_reproduccion = base_de_datos.Column(base_de_datos.Integer, primary_key=True)
    nombre = base_de_datos.Column(base_de_datos.String(70), nullable=False)
    descripcion = base_de_datos.Column(base_de_datos.String(300))
    duracion_total = base_de_datos.Column(base_de_datos.Integer, default=0)
    usuario_id = base_de_datos.Column(base_de_datos.Integer, base_de_datos.ForeignKey('usuario.id_usuario'),
                                      nullable=False)
    canciones = base_de_datos.relationship('Cancion',
                                           secondary=canciones_de_listas_reproduccion, lazy='subquery',
                                           backref=base_de_datos.backref('cancion', lazy=True))

    def guardar(self):
        """
        Guarda en la base de datos el objeto actual
        :return: None
        """
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def editar(self, nombre, descripcion):
        """
        Edita la informacion del objeto actual
        :param nombre: El nuevo nombre que tendra la lista de reproduccion
        :param descripcion: La nueva descripcion que tendra la lista
        :return: None
        """
        if nombre is not None:
            self.nombre = nombre
        if descripcion is not None:
            self.descripcion = descripcion
        base_de_datos.session.commit()

    def eliminar(self):
        """
        Elimina el objeto actual de la base de datos
        :return: None
        """
        base_de_datos.session.delete(self)
        base_de_datos.session.commit()

    def agregar_cancion(self, cancion):
        """
        Agrega una cancion a la lista de reproduccion
        :param cancion: La cancion a agregar
        :return: None
        """
        self.canciones.append(cancion)
        if self.duracion_total is None:
            self.duracion_total = 0
        self.duracion_total += cancion.duracion_en_segundos
        base_de_datos.session.commit()

    @staticmethod
    def obtener_listas_de_reproduccion_de_usuario(id_usuario):
        """
        Recupera de la base de datos todas las listas de reproduccion de un usuario
        :param id_usuario: El id del usuario del cual se van a recuperar sus listas de reproduccion
        :return: Una lista de Lista de reproduccion
        """
        listas_de_reproduccion = ListaDeReproduccion.query.filter_by(usuario_id=id_usuario).all()
        return listas_de_reproduccion

    @staticmethod
    def obtener_lista_de_reproduccion(id_lista_de_reproduccion):
        """
        Recupera la lista de reproduccion con el id lista de reproduccion y el id usuario
        :param id_lista_de_reproduccion: El id de la lista de reproduccion a validar
        :return: Una ListaDeReproduccion
        """
        lista_de_reproduccion = ListaDeReproduccion.query.\
            filter_by(id_lista_de_reproduccion=id_lista_de_reproduccion).first()
        return lista_de_reproduccion

    def obtener_json(self):
        """
        Genera un diccionario con los atributos del objeto
        :return: Un diccionario
        """
        diccionario = {'id': self.id_lista_de_reproduccion, 'nombre': self.nombre, 'descripcion': self.descripcion,
                       'duracion_total': self.duracion_total}
        return diccionario

    @staticmethod
    def validar_existe_lista_de_reproduccion(id_lista_de_reproduccion):
        """
        Valida si existe una lista con el id indicado
        :param id_lista_de_reproduccion: El id de la lista de reproduccion a validar si existe
        :return: Verdadero si existe el una lista con el id indicado o False si no existe
        """
        cantidad_listas = ListaDeReproduccion.query.filter_by(id_lista_de_reproduccion=id_lista_de_reproduccion).count()
        return cantidad_listas > 0

    @staticmethod
    def validar_usuario_es_dueno_de_lista_de_reproduccion(id_lista_reproduccion, id_usuario):
        """
        Valida si el usuario con el id usuario es dueño de la lista de reproduccion con el id lista reproduccion
        :param id_lista_reproduccion: El id de la lista de reproduccion a validar
        :param id_usuario: El id del usuario a validar si es dueño de la cancion
        :return: Vardadero si el usuario es dueño de la cancion
        """
        cantidad_listas = ListaDeReproduccion.query.filter_by(id_lista_de_reproduccion=id_lista_reproduccion,
                                                              usuario_id=id_usuario).count()
        return cantidad_listas > 0
