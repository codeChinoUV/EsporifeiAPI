FROM python:3
COPY ConvertidorDeArchivosServer.py .
ADD requerimientos.txt .
RUN mkdir protos convertidor_de_canciones
RUN mkdir canciones
COPY protos/ConvertidorDeArchivos.proto ./protos
COPY convertidor_de_canciones/__init__.py ./convertidor_de_canciones
COPY convertidor_de_canciones/ConvertidorDeCanciones.py ./convertidor_de_canciones

RUN pip3 install -r ./requerimientos.txt
RUN ls -l
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/ConvertidorDeArchivos.proto
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y ffmpeg
RUN touch EspotifeiConvertidorDeArchivos.log
EXPOSE 5002
CMD ["python3", "ConvertidorDeArchivosServer.py"]
# RUN ["tail", "-f", "EspotifeiConvertidorDeArchivos.log"]