import os

# Получаем абсолютный путь к папке проекта
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    # Настройка базы данных SQLite (файл появится в папке проекта)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'urban.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Секретный ключ для сессий Flask (для безопасности)
    SECRET_KEY = 'Супер_глеб_2007'