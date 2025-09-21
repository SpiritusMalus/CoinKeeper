FROM python:3.11

WORKDIR /app
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости первыми для лучшего кэширования
COPY app/config/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY app/ .

# Копируем alembic.ini из корня проекта
COPY alembic.ini .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]