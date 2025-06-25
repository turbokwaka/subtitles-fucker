# main_window.py

import os

import cv2
from PyQt6.QtGui import QIcon, QFontDatabase, QImage, QPixmap
from PyQt6.QtWidgets import QMainWindow

from config import STYLESHEET

def frame_to_pixmap(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    h_max = 360
    w_max = 640
    resized = cv2.resize(rgb, (w_max, h_max), interpolation=cv2.INTER_AREA)

    h, w, ch = resized.shape

    bytes_per_line = ch * w
    image = QImage(resized.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
    print(h, w, ch)
    return QPixmap.fromImage(image)

def load_and_show_first_frame(video_path, label_widget):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    cap.release()
    if success:
        pixmap = frame_to_pixmap(frame)
        label_widget.setPixmap(pixmap)
        label_widget.original_pixmap = pixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ти уйобіще, закрий мене")
        self.setFixedWidth(680)
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
