# Используем официальный легковесный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y netcat-openbsd

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт entrypoint
COPY entrypoint.sh /app/

# Копируем код приложения
COPY . /app/

# Устанавливаем скрипт entrypoint
RUN chmod +x /app/entrypoint.sh

# Устанавливаем переменную окружения для корректного вывода
ENV PYTHONUNBUFFERED=1

# Устанавливаем скрипт entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
