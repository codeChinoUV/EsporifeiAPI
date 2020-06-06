"""
    Se encarga de representar a un USUARIO y manejar el acceso del objeto a la base de datos
"""
from werkzeug.security import generate_password_hash, check_password_hash

from app import base_de_datos
from app.manejo_de_usuarios.modelo.enum.enums import TipoUsuario


class Usuario(base_de_datos.Model):
    """
    Se encarga de representar el modelo usuario y define su estructura en la base de datos
    """
    id_usuario = base_de_datos.Column(base_de_datos.Integer, primary_key=True)
    nombre_usuario = base_de_datos.Column(base_de_datos.String(20), unique=True, index=True)
    nombre = base_de_datos.Column(base_de_datos.String(70), nullable=False)
    contrasena = base_de_datos.Column(base_de_datos.String(80), nullable=False)
    tipo_usuario = base_de_datos.Column(base_de_datos.Integer, nullable=False)
    correo_electronico = base_de_datos.Column(base_de_datos.String(100), nullable=False, unique=True)

    def guardar(self):
        """
        Guarda la informacion del objeto en la base de datos
        :return: None
        """
        self.contrasena = generate_password_hash(self.contrasena, method='sha256')
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def editar(self, nombre_usuario, nombre, contrasena, correo_electronico):
        """
        :param nombre_usuario: El nuevo nombre de usuario
        :param nombre: El nuevo nombre
        :param contrasena: La nueva contrasena
        :param correo_electronico: El nuevo correo electronico
        Actualiza la información de los atributos nombre_usuario, nombre, contrasena, correo_electronico y guarda los
        cambios realizados en la base de datos
        :return: None
        """
        if nombre_usuario is not None:
            self.nombre_usuario = nombre_usuario
        if nombre is not None:
            self.nombre = nombre
        if contrasena is not None:
            contrasena_hasheada = generate_password_hash(contrasena, method='sha256')
            self.contrasena = contrasena_hasheada
        if correo_electronico is not None:
            self.correo_electronico = correo_electronico
        base_de_datos.session.commit()

    @staticmethod
    def verificar_nombre_usuario_disponible(nombre_usuario):
        """
        Verifica si el nombre de usuario ya se encuentra en uso
        :param nombre_usuario: El nombre de usuario a validar
        :return: Verdadero si el nombre de usuario se encuentra disponible o falso si no
        """
        usuarios_con_el_mismo_nombre = Usuario.query.filter_by(nombre_usuario=nombre_usuario).count()
        return usuarios_con_el_mismo_nombre > 0

    def obtener_json(self):
        """
        Crea un diccionario que representa al objeto a partir de la información del mismo
        :return: Un diccionario con la información del objeto
        """
        json = {'nombre_usuario': self.nombre_usuario, 'contrasena': None, 'nombre': self.nombre,
                'correo_electronico': self.correo_electronico, 'tipo_usuario': self.tipo_usuario}
        return json

    @staticmethod
    def validar_usuario_creador_de_contenido(nombre_usuario):
        """
        Valida que el usuario sea de tipo creador de contenido
        :param nombre_usuario: El nombre_usuario a validar
        :return: Verdadero si el usuario es creador de contenido o falso si no
        """
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        return TipoUsuario(usuario.tipo_usuario) == TipoUsuario.CreadorDeContenido

    @staticmethod
    def obtener_usuario_por_id(id_usuario):
        """
        Recupera al usuario que tenga el id_usuario
        :param id_usuario: El id del usuario a recuperar
        :return: El usuario que tenga el id_usuario o None si ningun usuario tiene el id_usuario
        """
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        return usuario

    @staticmethod
    def obtener_usuario(nombre_usuario):
        """
        Recupera al usuario de la base de datos que tiene el nombre_usuario
        :param nombre_usuario: El nombre del usuario a recueprar
        :return: El usuario que tiene el nombre de usuario
        """
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        return usuario

    @staticmethod
    def validar_credenciales(nombre_usuario, contrasena):
        """
        Valida que las credenciales de un usuario sean correctas
        :param nombre_usuario: El nombre del usuario a validar que sea correcto
        :param contrasena: La contrasena que pertenece al nombre de usuario
        :return: El usuario al que pertenecen las credenciaels o None si las credenciales no pertenecen a nadie
        """
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if check_password_hash(usuario.contrasena, contrasena):
            return usuario

    @staticmethod
    def validar_correo_electronico_disponible(correo_electronico):
        """
        Valida si el correo electronico se encuentra disponibles
        :param correo_electronico: El correo electronico a validar si se encuentra disponible
        :return: Verdadero si se encuentra disponible, falso si no
        """
        cantidad_correos_electronicos_iguales = Usuario.query.filter_by(correo_electronico=correo_electronico).count()
        return cantidad_correos_electronicos_iguales == 0
