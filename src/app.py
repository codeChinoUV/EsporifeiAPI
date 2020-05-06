from src import app, base_de_datos
from src.administracion_de_contenido.controlador.v1.CreadorDeContenidoControlador import CreadorDeContenidoControlador\
    , ArtistasControlador
from src.administracion_de_contenido.controlador.v1.CreadorDeContenidoUsuarioControlador import \
    CreadorDeContenidoUsuarioControlador
from src.administracion_de_contenido.controlador.v1.CreadoresDeContenidoUsuarioControlador import \
    CreadoresDeContenidoControlador
from src.administracion_de_contenido.controlador.v1.CreadoresDeContenidoControlador import \
    CreadoresDeContenidoBuscarControlador
from src.manejo_de_usuarios.controlador.v1.LoginControlador import LoginControlador
from src.manejo_de_usuarios.controlador.v1.UsuariosControlador import UsuariosControlador

#Exponer endpoint login
LoginControlador.exponer_endpoint(app)

#Expones endpoint de usuarios
UsuariosControlador.exponer_end_point(app)

#Exponemos endpoint de creadores de contenido
CreadorDeContenidoControlador.exponer_end_point(app)
CreadoresDeContenidoControlador.exponer_end_point(app)
CreadoresDeContenidoBuscarControlador.exponer_end_point(app)
ArtistasControlador.exponer_end_point(app)

#Exponemos endpoint para usuarios de creadores de contenido
CreadorDeContenidoUsuarioControlador.exponer_end_point(app)

#Creacion base de datos
base_de_datos.create_all()

base_de_datos.create_all()
if __name__ == '__main__':
    app.run(debug=True)
