FROM python:3
WORKDIR WORKDIR /usr/src/app
RUN echo "Copiando aplicacion"
RUN mkdir app
RUN mkdir app/administracion_de_contenido
RUN mkdir app/manejo_de_archivos
RUN mkdir app/manejo_de_usuarios
RUN mkdir app/util
RUN mkdir config
RUN mkdir migrations
COPY app/administracion_de_contenido app/administracion_de_contenido
COPY app/manejo_de_archivos app/manejo_de_archivos
COPY app/manejo_de_usuarios app/manejo_de_usuarios
COPY app/util app/util
COPY app/__init__.py app/
COPY app/entry-docker.sh .
COPY config config/
COPY migrations migrations/
COPY entrypoint.py .
COPY requerimientos.txt .

RUN echo "Instalando software"
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3-pip postgresql-contrib libpq-dev ffmpeg

RUN apt-get update && apt-get -y install sudo
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

RUN pip3 install -r ./requerimientos.txt
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. app/manejo_de_archivos/protos/ManejadorDeArchivos.proto
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. app/manejo_de_archivos/protos_convertidor_de_archivos/ConvertidorDeArchivos.proto
ENV FLASK_APP="entrypoint.py"
ENV APP_SETTINGS_MODULE="config.prod"
ENV FLASK_ENV="production"
ENV GRPC_PORT=5001
ENV MONGO_IP="mongo_db"
ENV CONVERTIDOR_ARCHIVOS_IP="convertidor_archivos"
ENV CONVERTIDOR_ARCHIVOS_PORT=5002
RUN echo $APP_SETTINGS_MODULE
EXPOSE 5000
EXPOSE 5001
ENTRYPOINT ["app/entry-docker.sh"]
