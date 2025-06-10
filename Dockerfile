# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Копируем все файлы бота в контейнер
COPY bot.py .
COPY baza.py .
COPY callbacks.py .
COPY cfg.py .
COPY funcs_markup.py .
COPY requirements.txt .
COPY DATA.db .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем SQLite базу данных в /app
# COPY DATA.db /app/DATA.db

# Команда для запуска вашего бота
CMD ["python", "-u", "/app/bot.py"]
