from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication


def set_application_style(app):
    """Установка стилей для всего приложения"""
    app.setStyle("Fusion")

    # Создание палитры
    palette = QPalette()

    # Основные цвета
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(33, 33, 33))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(33, 33, 33))
    palette.setColor(QPalette.ColorRole.Text, QColor(33, 33, 33))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(33, 33, 33))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(66, 133, 244))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

    app.setPalette(palette)

    # Установка глобальных стилей
    app.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }

        QMenuBar {
            background-color: #f5f5f5;
            border-bottom: 1px solid #ddd;
        }

        QMenuBar::item {
            padding: 5px 10px;
        }

        QMenuBar::item:selected {
            background-color: #e0e0e0;
        }

        QMenu {
            background-color: white;
            border: 1px solid #ddd;
        }

        QMenu::item:selected {
            background-color: #e3f2fd;
        }

        QToolTip {
            background-color: #fffde7;
            color: #333;
            border: 1px solid #ffd54f;
            padding: 5px;
        }
    """)


# Стили для окна входа
ROLE_PANEL_STYLE = """
    QWidget {
        background-color: white;
        border-radius: 15px;
        border: 2px solid #bbdefb;
    }
    QWidget:hover {
        border-color: #3949ab;
        background-color: #f9f9f9;
    }
"""

ROLE_LABEL_STYLE = """
    QLabel {
        color: #1a237e;
        font-size: 20px;
        font-weight: bold;
        padding: 5px;
    }
"""

DESC_ROLE_STYLE = """
    QLabel {
        color: #455a64;
        font-size: 13px;
        line-height: 1.4;
    }
"""

INPUT_STYLE = """
    QLineEdit {
        padding: 10px 15px;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        font-size: 14px;
        background-color: #fafafa;
    }
    QLineEdit:focus {
        border-color: #3949ab;
        background-color: white;
    }
"""

CHECKBOX_STYLE = """
    QCheckBox {
        color: #546e7a;
        font-size: 13px;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }
    QCheckBox::indicator:checked {
        background-color: #3949ab;
        border: 2px solid #3949ab;
        border-radius: 3px;
    }
"""

LOGIN_BUTTON_STYLE = """
    QPushButton {
        background-color: #3949ab;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-size: 14px;
        font-weight: bold;
        margin-top: 10px;
    }
    QPushButton:hover {
        background-color: #303f9f;
    }
    QPushButton:pressed {
        background-color: #283593;
    }
    QPushButton:disabled {
        background-color: #bbdefb;
        color: #78909c;
    }
"""

TEST_LABEL_STYLE = """
    QLabel {
        color: #78909c;
        font-size: 11px;
        font-style: italic;
        padding: 5px;
    }
"""

QUICK_LOGIN_STYLE = """
    QPushButton {
        background-color: transparent;
        color: #3949ab;
        border: 1px solid #3949ab;
        border-radius: 6px;
        padding: 8px;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: #e8eaf6;
    }
"""

WELCOME_LABEL_STYLE = """
    QLabel {
        color: #1a237e;
        font-size: 28px;
        font-weight: bold;
        padding: 10px;
    }
"""

DESC_LABEL_STYLE = """
    QLabel {
        color: #455a64;
        font-size: 16px;
        padding: 5px 20px;
    }
"""

DEMO_BUTTON_STYLE = """
    QPushButton {
        background-color: #ff9800;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #f57c00;
    }
"""

ADMIN_BUTTON_STYLE = """
    QPushButton {
        background-color: #d32f2f;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #c62828;
    }
"""

# Стили для диалога администратора
ADMIN_TITLE_STYLE = """
    QLabel {
        color: #d32f2f;
        font-size: 18px;
        font-weight: bold;
    }
"""

ADMIN_INPUT_STYLE = """
    QLineEdit {
        padding: 12px 15px;
        border: 2px solid #ffcdd2;
        border-radius: 8px;
        font-size: 14px;
        background-color: #fff;
    }
    QLineEdit:focus {
        border-color: #d32f2f;
    }
"""

ADMIN_LOGIN_BUTTON_STYLE = """
    QPushButton {
        background-color: #d32f2f;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #c62828;
    }
"""

ADMIN_CANCEL_BUTTON_STYLE = """
    QPushButton {
        background-color: #757575;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #616161;
    }
"""
