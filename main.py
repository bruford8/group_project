import sys
import os
from PyQt6.QtWidgets import QApplication

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.login_window import LoginWindow


def main():
    """Главная функция запуска приложения"""
    app = QApplication(sys.argv)

    # Установка стиля приложения
    app.setStyle("Fusion")

    # Создание и отображение окна входа
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())
