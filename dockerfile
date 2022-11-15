FROM python:3.10-slim-bullseye AS build 
RUN apt-get update
RUN apt-get install -y curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /opt/todoapp/
COPY poetry.toml /opt/todoapp/
COPY pyproject.toml /opt/todoapp/
COPY poetry.lock /opt/todoapp/
RUN poetry install
EXPOSE 8000


FROM build AS prod

COPY todo_app/ /opt/todoapp/todo_app

#ENTRYPOINT ["poetry", "run"]

CMD poetry run gunicorn "todo_app.app:create_app()" "--bind 0.0.0.0:{$PORT:-8000}"

#to-run: docker run -e DEV=0  --env-file .env  -p 80:8000 todo-app:prod

FROM build AS dev


ENTRYPOINT ["poetry", "run"]
CMD ["flask", "run"]





#to-run docker run -e DEV=1 --env-file .env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/opt/todoapp/todo_app todo-app:dev
 
FROM build AS test

COPY todo_app/ /opt/todoapp/todo_app
COPY tests/ /opt/todoapp/tests
CMD ["poetry", "run","pytest"]

#to-run: docker run -e DEV=0  --env-file .env.test  -p 80:8000 todo-app:test