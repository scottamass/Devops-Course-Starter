FROM centos/python-38-centos7:latest
RUN apt-get update && apt-get install -y \curl
RUN  curl -sSL https://install.python-poetry.org | python3
RUN mk dir /opt/todoapp/
WORKDIR /opt/code
COPY . /opt/code