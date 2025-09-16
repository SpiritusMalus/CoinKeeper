FROM python:3.11

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements из другой папки
COPY config/requirements/requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов приложения
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]