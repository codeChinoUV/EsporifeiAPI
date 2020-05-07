from src import app, base_de_datos
from src.administracion_de_contenido.controlador.v1.CreadorDeContenidoControlador import CreadorDeContenidoControlador \
    , ArtistasControlador, ArtistaControlador, CreadorDeContenidoPublicoControlador, ArtistasPublicoControlador
from src.administracion_de_contenido.controlador.v1.CreadoresDeContenidoControlador import \
    CreadoresDeContenidoBuscarControlador
from src.manejo_de_usuarios.controlador.v1.LoginControlador import LoginControlador
from src.manejo_de_usuarios.controlador.v1.UsuarioControlador import UsuarioControlador

# Exponer endpoint login
LoginControlador.exponer_endpoint(app)

# Exponemos endpoint usuario
UsuarioControlador.exponer_endpoint(app)

# Exponemos endpoint de creadores de contenido
CreadorDeContenidoControlador.exponer_end_point(app)
CreadoresDeContenidoBuscarControlador.exponer_end_point(app)
CreadorDeContenidoPublicoControlador.exponer_endpoint(app)
ArtistasControlador.exponer_end_point(app)
ArtistaControlador.exponer_endpoint(app)
ArtistasPublicoControlador.exponer_endpoint(app)

# Creacion base de datos
base_de_datos.create_all()

base_de_datos.create_all()
if __name__ == '__main__':
    app.run(debug=True)
