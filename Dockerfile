FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Системные зависимости для pytesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-all && \
    rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY . .

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

# Пробрасываем порт
EXPOSE 8001

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
