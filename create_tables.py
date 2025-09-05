#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

# Добавляем путь к приложению
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from app.database import engine, Base
from app import models

def create_tables():
    print("Создание таблиц базы данных...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы!")

if __name__ == "__main__":
    create_tables()