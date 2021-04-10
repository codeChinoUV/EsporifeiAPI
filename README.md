# EspotifeiAPI
EspotifeiAPI es una API REST para el consumo musical, Espotifei permite a sus usuarios el manejo de:

- Creadores de contenido
- Álbumes
- Canciones
- Listas de reproducción
- Canciones personales

Además de permitir el envió de canciones en diferentes calidades, la reproducción de la “radio” de una canción 
entre otras funcionalidades.

Despliegue:
1. Modifica las variables de entorno de la base de datos que se encuentran docker-compose.yml
```
  POSTGRES_USER: PON_UN_USUARIO
  POSTGRES_PASSWORD: PON_UNA_CONTRASEÑA
  POSTGRES_DB: PON_UNA_DB
```
2. Modifica el archivo de variables de entorno de la configuración de producción que se encuentra en /config/prod.py
```
  SECRET_KEY = 'ponunallavesecretaaqui'
  SQLALCHEMY_DATABASE_URI = "postgresql://PON_TU_USUARIO:PON_TU_CONTRASEÑA@psql_db:5432/PON_EL_NOMBRE_DE_LA_BD"

```
3. Agrega el permiso de ejecución al archivo de entry-docker.sh que se encuentra en /app/entry-docker.sh
```
  chmod +x entry-docker.sh
```
4. Crear y levantar los contenedores de docker
```
  docker-compose up --build 
```

Nota: en caso de querer modificar otras configuraciones verificar las variables de entorno del archivo Dockerfile
