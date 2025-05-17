FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install 'uvicorn[standard]'
RUN pip install 'fastapi[standard]'

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir -r requirements.txt

# RUN patchright install --with-deps

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "info"]