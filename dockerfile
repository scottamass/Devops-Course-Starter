FROM python:3.10-slim-bullseye
RUN apt-get update
RUN apt-get install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV POETRY_HOME="/opt/poetry" 
ENV PATH="${PATH}:/root/.poetry/bin"
RUN mkdir /opt/todoapp/
WORKDIR /opt/code
COPY . /opt/code 
RUN poetry install

EXPOSE 5000

ENTRYPOINT ["poetry", "run"]
CMD ["flask","run","--host=0.0.0.0"]