FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential default-libmysqlclient-dev

COPY pyproject.toml .

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
