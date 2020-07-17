FROM python:3.8.3-slim
WORKDIR /usr/src/app
RUN mkdir convertidor_archivos
COPY ConvertidorDeArchivosServer.py ./convertidor_archivos
ADD requerimientos.txt ./convertidor_archivos
RUN mkdir convertidor_archivos/protos convertidor_archivos/convertidor
RUN mkdir convertidor_archivos/canciones
COPY protos/ConvertidorDeArchivos.proto ./convertidor_archivos/protos
COPY convertidor ./convertidor_archivos/convertidor

RUN pip3 install -r ./requerimientos.txt
RUN ls -l
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/ConvertidorDeArchivos.proto
COPY protos/ ./convertidor_archivos/protos
RUN ls -l protos
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y ffmpeg
RUN touch EspotifeiConvertidorDeArchivos.log
EXPOSE 5002
CMD ["python3", "ConvertidorDeArchivosServer.py"]
