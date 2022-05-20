FROM python:3.10-slim-bullseye AS build 
RUN apt-get update
RUN apt-get install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV POETRY_HOME="/opt/poetry" 
ENV PATH="${PATH}:/root/.poetry/bin"
RUN mkdir /opt/todoapp/
WORKDIR /opt/todoapp/
COPY poetry.toml /opt/todoapp/
COPY pyproject.toml /opt/todoapp/
COPY poetry.lock /opt/todoapp/

EXPOSE 8000
ENV EnvironmentFile=/opt/todoapp/.env

FROM build AS prod

COPY todo_app/. /opt/todoapp/todo_app
RUN poetry install
ENTRYPOINT ["poetry", "run"]

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "todo_app.app:create_app()"]

#to-run: docker run  --env-file .env  -p 80:8000 todo-app:prod

FROM build as dev

RUN poetry install
ENTRYPOINT ["poetry", "run"]
CMD ["flask", "run","--host=0.0.0.0"]


#to-run docker run --env-file .env -p 5000:80 --mount type=bind,source="$(pwd)"/todo_app,target=/opt/todoapp/todo_app todo-app:dev
 
