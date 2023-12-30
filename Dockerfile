FROM python:latest

ADD oracli/oracli.py .
ADD pyproject.toml .
ADD poetry.lock .
RUN pip install poetry
RUN poetry install
ENTRYPOINT ["poetry", "run", "python", "oracli.py",]