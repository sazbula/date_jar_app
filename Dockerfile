FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

EXPOSE 8000

CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]