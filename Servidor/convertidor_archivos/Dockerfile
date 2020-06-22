FROM python:3

ADD ConvertidorDeArchivosServer.py /
ADD requerimientos.txt /
ADD protos/ConvertidorDeArchivos.proto /

RUN pip install -r requerimientos.txt
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/ConvertidorDeArchivos.proto
RUN apt-get update
RUN apt-get upgrade -y

EXPOSE 5002
CMD["python", "ConvertidorDeArchivosServer.py"]
CMD["tail", "-f", "EspotifeiConvertidorDeArchivos.log"]