FROM python:3.12-slim

# Install system build tools and Postgres deps + bcrypt deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    gcc

WORKDIR /app

COPY requirements.txt /app/

# Fix bcrypt issue by installing a stable version first
RUN pip install --no-cache-dir bcrypt==4.0.1

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]