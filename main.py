# main.py

import sys

from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
