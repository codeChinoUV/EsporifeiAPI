FROM python:3.8.3-slim
WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requerimientos.txt
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/ConvertidorDeArchivos.proto
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y ffmpeg
RUN touch EspotifeiConvertidorDeArchivos.log
EXPOSE 5002
CMD ["python3", "ConvertidorDeArchivosServer.py"]
