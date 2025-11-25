FROM python:3.13.9-slim-trixie

WORKDIR /app

COPY requirements.txt .
COPY openapi.yml .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
