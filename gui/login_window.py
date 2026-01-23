from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import os

# Добавляем пути для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import UserRole
from services.auth_service import AuthService
from services.diary_service import DiaryService
from database import Database


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.auth_service = None
        self.diary_service = None
        self.current_user = None
        self.init_services()
        self.setup_ui()

    def init_services(self):
        """Инициализация сервисов и базы данных"""
        try:
            self.db = Database("school_system.db")
            self.auth_service = AuthService(self.db)
            self.diary_service = DiaryService(self.db)

            # Создание тестовых пользователей и данных
            self.auth_service.create_test_users()
            self.diary_service.create_test_data()

            print("Сервисы успешно инициализированы")
        except Exception as e:
            print(f"Ошибка инициализации сервисов: {e}")
            QMessageBox.critical(self, "Ошибка",
                                 f"Не удалось инициализировать систему: {str(e)}")

    def setup_ui(self):
        """Настройка интерфейса окна входа"""
        self.setWindowTitle("Школьная образовательная система")
        self.setFixedSize(1000, 700)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Верхняя панель
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)

        # Основной контент
        content_widget = self.create_content()
        main_layout.addWidget(content_widget)

        # Нижняя панель
        footer_widget = self.create_footer()
        main_layout.addWidget(footer_widget)

    def create_header(self):
        """Создание верхней панели"""
        widget = QWidget()
        widget.setFixedHeight(70)
        widget.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                border-bottom: 3px solid #3498db;
            }
        """)

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(20, 10, 20, 10)

        # Логотип и название
        logo_label = QLabel("🏫 ШКОЛЬНАЯ СИСТЕМА")
        logo_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)

        layout.addWidget(logo_label)
        layout.addStretch()

        return widget

    def create_content(self):
        """Создание основного контента"""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
            }
        """)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        # Заголовок
        title_label = QLabel("ВХОД В СИСТЕМУ")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 28px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title_label)

        # Контейнер для панелей входа
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setSpacing(30)

        # Панели для разных ролей
        roles = [
            ("🎒", "Ученик", "student", "#3498db"),
            ("👨‍👩‍👧‍👦", "Родитель", "parent", "#2ecc71"),
            ("👨‍🏫", "Учитель", "teacher", "#e74c3c")
        ]

        for emoji, name, role_type, color in roles:
            panel = self.create_login_panel(emoji, name, role_type, color)
            container_layout.addWidget(panel)

        layout.addWidget(container)

        # Панель администратора
        admin_panel = self.create_admin_panel()
        layout.addWidget(admin_panel, alignment=Qt.AlignmentFlag.AlignCenter)

        return widget

    def create_login_panel(self, emoji, name, role_type, color):
        """Создание панели входа для конкретной роли"""
        widget = QWidget()
        widget.setFixedWidth(280)
        widget.setMinimumHeight(400)

        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Стиль панели
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-radius: 10px;
                border: 2px solid {color};
            }}
        """)

        # Иконка
        icon_label = QLabel(emoji)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px;")
        layout.addWidget(icon_label)

        # Название
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 20px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(name_label)

        # Разделитель
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"background-color: {color}; margin: 10px 0;")
        layout.addWidget(line)

        # Поля ввода
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        # Логин
        username_edit = QLineEdit()
        username_edit.setPlaceholderText("Имя пользователя")
        username_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)

        # Пароль
        password_edit = QLineEdit()
        password_edit.setPlaceholderText("Пароль")
        password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        password_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)

        form_layout.addWidget(username_edit)
        form_layout.addWidget(password_edit)
        layout.addLayout(form_layout)

        # Тестовые данные
        test_data = self.get_test_data(role_type)
        test_label = QLabel(f"Тест: {test_data}")
        test_label.setStyleSheet("color: #7f8c8d; font-size: 12px; font-style: italic;")
        test_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(test_label)

        # Кнопка входа
        login_button = QPushButton("Войти")
        login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                margin-top: 10px;
            }}
            QPushButton:hover {{
                background-color: {'#2980b9' if color == '#3498db' else
        '#27ae60' if color == '#2ecc71' else
        '#c0392b'};
            }}
        """)

        # Подключаем кнопку
        login_button.clicked.connect(
            lambda: self.login(username_edit.text(), password_edit.text(), role_type)
        )

        layout.addWidget(login_button)
        layout.addStretch()

        return widget

    def create_admin_panel(self):
        """Создание панели администратора"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        admin_button = QPushButton("⚙ Панель администратора")
        admin_button.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7d3c98;
            }
        """)
        admin_button.clicked.connect(self.show_admin_login)

        layout.addWidget(admin_button)
        return widget

    def create_footer(self):
        """Создание нижней панели"""
        widget = QWidget()
        widget.setFixedHeight(40)
        widget.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                border-top: 1px solid #34495e;
            }
        """)

        layout = QHBoxLayout(widget)

        version_label = QLabel("© 2024 Школьная система v1.0")
        version_label.setStyleSheet("color: #bdc3c7; font-size: 12px;")

        layout.addWidget(version_label)
        layout.addStretch()

        return widget

    def get_test_data(self, role_type):
        """Возвращает тестовые данные для роли"""
        data = {
            "student": "student_petrov / student123",
            "parent": "parent_sidorov / parent123",
            "teacher": "teacher_ivanov / teacher123"
        }
        return data.get(role_type, "")

    def login(self, username, password, role_type):
        """Обработка входа пользователя"""
        if not username or not password:
            QMessageBox.warning(self, "Ошибка",
                                "Введите имя пользователя и пароль")
            return

        user = self.auth_service.login(username, password)

        if user:
            # Проверяем соответствие роли
            role_mapping = {
                "student": UserRole.STUDENT,
                "parent": UserRole.PARENT,
                "teacher": UserRole.TEACHER,
                "admin": UserRole.ADMIN
            }

            expected_role = role_mapping.get(role_type)

            if user.role == expected_role:
                self.current_user = user
                QMessageBox.information(self, "Успех",
                                        f"Добро пожаловать, {user.full_name}!")
                # Здесь можно открыть соответствующее окно
            else:
                QMessageBox.warning(self, "Ошибка",
                                    f"Эта учетная запись не является {role_type}")
        else:
            QMessageBox.warning(self, "Ошибка",
                                "Неверное имя пользователя или пароль")

    def show_admin_login(self):
        """Показать диалог входа администратора"""
        dialog = AdminLoginDialog(self.auth_service, self)
        if dialog.exec():
            user = dialog.get_user()
            if user:
                QMessageBox.information(self, "Успех",
                                        f"Добро пожаловать, администратор {user.full_name}!")


class AdminLoginDialog(QDialog):
    def __init__(self, auth_service, parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.user = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Вход администратора")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        title_label = QLabel("АДМИНИСТРАТОР")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #8e44ad;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title_label)

        # Поля ввода
        form_layout = QVBoxLayout()

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Имя администратора")

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Пароль")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addWidget(self.username_edit)
        form_layout.addWidget(self.password_edit)
        layout.addLayout(form_layout)

        # Кнопки
        button_layout = QHBoxLayout()

        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.authenticate)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
        """)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(login_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Тестовые данные
        test_label = QLabel("Тестовые данные: admin / admin123")
        test_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        test_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(test_label)

    def authenticate(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        user = self.auth_service.login(username, password)
        if user and user.role == UserRole.ADMIN:
            self.user = user
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка",
                                "Неверные данные администратора")

    def get_user(self):
        return self.user


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())
