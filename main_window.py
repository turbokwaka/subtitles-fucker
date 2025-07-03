# main_window.py

import os

from PyQt6.QtGui import QIcon, QFontDatabase
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt6.QtCore import QThread

from config import STYLESHEET
from transcribe_worker import TranscribeWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ти уйобіще, закрий мене")
        self.setFixedWidth(1400)
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

    def start_transcription(self):

        if not self.video_player.video_path:
            QMessageBox.warning(self, "Помилка", "Спочатку завантаж відео!")
            return
        if not self.crop_rect:
            QMessageBox.warning(self, "Помилка", "Не виділена область на відео.")
            return

        self.gif_label.show()
        self.subtitles_output.setText("")
        self.start_button.setEnabled(False)

        x0, y0, x1, y1 = self.crop_rect
        lang = self.select_lang.currentData()
        frames_skip = int(self.select_frames_skip.currentText())

        self.thread = QThread()
        self.worker = TranscribeWorker(
            video_path=self.video_player.video_path,
            frames_to_skip=frames_skip,
            lang=lang,
            crop_x=x0,
            crop_y=y0,
            crop_width=x1 - x0,
            crop_height=y1 - y0,
        )
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        def on_finished(success, msg):
            self.gif_label.hide()
            self.start_button.setEnabled(False)
            self.subtitles_output.setText(msg)

        self.worker.finished.connect(on_finished)
        self.thread.start()