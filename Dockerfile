FROM python:3.11-slim

ENV POETRY_VERSION=1.7.1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false \
  && poetry install --no-root --no-interaction --no-ansi
COPY . .

#ENTRYPOINT ["bash", "entrypoint.sh"]

EXPOSE 8000
