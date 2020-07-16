FROM python:3.8.3-slim
WORKDIR /usr/src/app
COPY ConvertidorDeArchivosServer.py .
ADD requerimientos.txt .
RUN mkdir protos convertidor
RUN mkdir canciones
COPY protos/ConvertidorDeArchivos.proto ./protos
COPY convertidor ./convertidor
COPY convertidor ./convertidor

RUN pip3 install -r ./requerimientos.txt
RUN ls -l
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/ConvertidorDeArchivos.proto
COPY protos/ ./protos
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y ffmpeg
RUN touch EspotifeiConvertidorDeArchivos.log
EXPOSE 5002
CMD ["python3", "ConvertidorDeArchivosServer.py"]