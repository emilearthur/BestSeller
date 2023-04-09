FROM python:3.11.2-slim

WORKDIR /code

RUN pip install poetry==1.3.2


COPY xml-parser-service/poetry.lock xml-parser-service/pyproject.toml /code/

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY xml-parser-service/xml_parser_service /code/xml_parser_service

ENV PYTHONPATH "${PYTHONPATH}:/xml_parser_service"