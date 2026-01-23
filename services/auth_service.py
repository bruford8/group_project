import hashlib
import secrets
import sqlite3
from typing import Optional
from models import User, UserRole


class AuthService:
    def __init__(self, db):
        self.db = db

    def hash_password(self, password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """Хэширование пароля с солью"""
        if salt is None:
            salt = secrets.token_hex(16)

        salted_password = password + salt
        password_hash = hashlib.sha256(salted_password.encode()).hexdigest()
        return password_hash, salt

    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Проверка пароля"""
        password_hash, _ = self.hash_password(password, salt)
        return password_hash == stored_hash

    def register(self, username: str, password: str,
                 full_name: str, role: UserRole,
                 class_id: Optional[int] = None,
                 email: Optional[str] = None,
                 phone: Optional[str] = None) -> Optional[User]:
        """Регистрация нового пользователя"""

        # Проверка существования пользователя
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                return None

        # Хэширование пароля
        password_hash, salt = self.hash_password(password)

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users 
                    (username, password_hash, salt, full_name, role, class_id, email, phone)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, password_hash, salt, full_name, role.value,
                      class_id, email, phone))

                user_id = cursor.lastrowid

                return User(
                    id=user_id,
                    username=username,
                    full_name=full_name,
                    role=role,
                    class_id=class_id,
                    email=email,
                    phone=phone
                )
            except sqlite3.IntegrityError as e:
                print(f"Ошибка регистрации: {e}")
                return None

    def login(self, username: str, password: str) -> Optional[User]:
        """Аутентификация пользователя"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, password_hash, salt, full_name, 
                       role, class_id, email, phone
                FROM users
                WHERE username = ?
            """, (username,))

            row = cursor.fetchone()
            if not row:
                return None

            # Проверка пароля
            if not self.verify_password(password, row['password_hash'], row['salt']):
                return None

            # Создание объекта пользователя
            return User(
                id=row['id'],
                username=row['username'],
                full_name=row['full_name'],
                role=UserRole(row['role']),
                class_id=row['class_id'],
                email=row['email'],
                phone=row['phone']
            )

    def create_test_users(self):
        """Создание тестовых пользователей для демонстрации"""
        test_users = [
            {
                'username': 'teacher_ivanov',
                'password': 'teacher123',
                'full_name': 'Иванов Иван Иванович',
                'role': UserRole.TEACHER,
                'class_id': 1,
                'email': 'ivanov@school.ru',
                'phone': '+79991234567'
            },
            {
                'username': 'student_petrov',
                'password': 'student123',
                'full_name': 'Петров Петр Петрович',
                'role': UserRole.STUDENT,
                'class_id': 1,
                'email': 'petrov@school.ru',
                'phone': '+79992345678'
            },
            {
                'username': 'parent_sidorov',
                'password': 'parent123',
                'full_name': 'Сидоров Сидор Сидорович',
                'role': UserRole.PARENT,
                'email': 'sidorov@mail.ru',
                'phone': '+79993456789'
            },
            {
                'username': 'admin',
                'password': 'admin123',
                'full_name': 'Администратор Системы',
                'role': UserRole.ADMIN,
                'email': 'admin@school.ru',
                'phone': '+79990000000'
            }
        ]

        for user_data in test_users:
            existing = self.login(user_data['username'], user_data['password'])
            if not existing:
                self.register(**user_data)
                print(f"Создан тестовый пользователь: {user_data['username']}")
