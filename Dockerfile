# Устанавливаем базовый образ
FROM python:3.11.0

# Устанавливаем зависимости проекта
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED 1

# Устанавливаем порт
EXPOSE 8000

# Запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]