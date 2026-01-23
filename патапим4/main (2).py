import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from computers_window import Schedule


def main():
    app = QApplication(sys.argv)

    window = Schedule()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()