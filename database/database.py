import sqlite3
import json
from contextlib import contextmanager
from datetime import datetime
from typing import Optional, List


class Database:
    def __init__(self, db_path: str = "school_system.db"):
        self.db_path = db_path
        self.init_database()

    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для подключения к БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_database(self):
        """Инициализация структуры базы данных"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Таблица пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    class_id INTEGER,
                    email TEXT,
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Таблица предметов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    teacher_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (teacher_id) REFERENCES users (id)
                )
            """)

            # Таблица оценок
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    subject_id INTEGER NOT NULL,
                    grade INTEGER NOT NULL,
                    date DATE NOT NULL,
                    comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES users (id),
                    FOREIGN KEY (subject_id) REFERENCES subjects (id)
                )
            """)

            # Таблица домашних заданий
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS homework (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_id INTEGER NOT NULL,
                    class_id INTEGER NOT NULL,
                    assignment_date DATE NOT NULL,
                    due_date DATE NOT NULL,
                    description TEXT NOT NULL,
                    attachments TEXT,  -- JSON массив
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (subject_id) REFERENCES subjects (id)
                )
            """)

            # Таблица классов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    teacher_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (teacher_id) REFERENCES users (id)
                )
            """)

            # Таблица посещаемости
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    status TEXT NOT NULL,
                    reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES users (id)
                )
            """)

            # Создание индексов для ускорения запросов
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_grades_student ON grades(student_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_grades_date ON grades(date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_homework_class ON homework(class_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_attendance_student ON attendance(student_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date)")

            # Создание триггера для обновления updated_at
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS update_users_timestamp 
                AFTER UPDATE ON users 
                FOR EACH ROW 
                BEGIN
                    UPDATE users SET updated_at = CURRENT_TIMESTAMP 
                    WHERE id = OLD.id;
                END;
            """)
