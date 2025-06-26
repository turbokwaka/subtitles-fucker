# main_window.py

import os

from PyQt6.QtGui import QIcon, QFontDatabase
from PyQt6.QtWidgets import QMainWindow

from config import STYLESHEET


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ти уйобіще, закрий мене")
        self.setFixedWidth(680)
        self.setFixedHeight(750)
        QFontDatabase.addApplicationFont("assets/Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont("assets/Montserrat-Bold.ttf")

        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        from ui_components import create_main_widget
        central_widget = create_main_widget(self)
        self.setStyleSheet(STYLESHEET)
        self.setCentralWidget(central_widget)
        print(self.width(), self.height())
