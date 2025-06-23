import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTextEdit, QMessageBox, QHBoxLayout, QComboBox, QSlider
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from videocr import save_subtitles_to_file

class Worker(QThread):
    finished = pyqtSignal(bool, str)  # успіх, повідомлення

    def __init__(self, video_path, frames_to_skip):
        super().__init__()
        self.video_path = video_path
        self.frames_to_skip = frames_to_skip

    def run(self):
        try:
            # перевіряєм чи вже існує output.srt
            # якщо так - видаляєм йо нахуй))
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(script_dir, "output.srt")
            if os.path.exists(output_path):
                os.remove(output_path)
                print("output.srt було знайдено і знищено.")

            save_subtitles_to_file(self.video_path,
                                   'output.srt',
                                   lang='en',
                                   time_start='0:00',
                                   time_end='2:00',
                                   frames_to_skip=self.frames_to_skip,
                                   sim_threshold=5
                                   )
            self.finished.emit(True, "Обробка завершена!")
        except Exception as e:
            self.finished.emit(False, f"Помилка: {str(e)}")

class SubtitleExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ти уйобіще, закрий мене")
        self.setFixedSize(666, 666)

        self.video_path = None

        self.settings_layout = QVBoxLayout()
        self.output_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()

        # SETTINGS
        self.vid_select_label = QLabel("Оберіть відеофайл для обробки:")
        self.vid_select_button = QPushButton("Обрати відео")
        self.vid_select_button.clicked.connect(self.browse_file)

        self.vid_select_layout = QVBoxLayout()
        self.vid_select_layout.addWidget(self.vid_select_label)
        self.vid_select_layout.addWidget(self.vid_select_button)

        self.lang_select_label = QLabel("Оберіть мову:")
        self.lang_selector = QComboBox()
        self.lang_selector.addItem("Українська", "ua")
        self.lang_selector.addItem("Англійська", "en")
        self.lang_selector.addItem("Японська", "jp")
        self.lang_selector.addItem("Китайська", "ch")
        self.lang_selector.setCurrentIndex(0)

        self.frames_to_skip_values = [1, 15, 30, 45, 60]

        self.frames_to_skip_label = QLabel(f"Скільки кадрів пропускати? ({self.frames_to_skip_values[0]})")
        self.frames_to_skip_slider = QSlider(Qt.Orientation.Horizontal)
        self.frames_to_skip_slider.setMinimum(0)
        self.frames_to_skip_slider.setMaximum(len(self.frames_to_skip_values) - 1)
        self.frames_to_skip_slider.setValue(0)
        self.frames_to_skip_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.frames_to_skip_slider.setTickInterval(1)

        def on_slider_change(index):
            actual_value = self.frames_to_skip_values[index]
            self.frames_to_skip_label.setText(f"Скільки кадрів пропускати? ({actual_value})")

        self.frames_to_skip_slider.valueChanged.connect(on_slider_change)

        self.frames_to_skip_layout = QVBoxLayout()
        self.frames_to_skip_layout.addWidget(self.frames_to_skip_label)
        self.frames_to_skip_layout.addWidget(self.frames_to_skip_slider)

        self.lang_select_layout = QVBoxLayout()
        self.lang_select_layout.addWidget(self.lang_select_label)
        self.lang_select_layout.addWidget(self.lang_selector)

        self.btn_start = QPushButton("Почати обробку")
        self.btn_start.clicked.connect(self.start_processing)
        self.btn_start.setEnabled(False)

        self.settings_layout.addLayout(self.vid_select_layout)
        self.settings_layout.addLayout(self.lang_select_layout)
        self.settings_layout.addLayout(self.frames_to_skip_layout)
        self.settings_layout.addStretch()
        self.settings_layout.addWidget(self.btn_start)

        # OUTPUT
        self.output_label = QLabel("Субтитри:")
        self.output_layout.addWidget(self.output_label)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.output_layout.addWidget(self.text_output)

        self.main_layout.addLayout(self.settings_layout)
        self.main_layout.addLayout(self.output_layout)

        self.setLayout(self.main_layout)
        self.worker = None
    def browse_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Відеофайли (*.mp4 *.avi *.mkv *.mov)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.video_path = selected_files[0].split("/")[-1]
                self.vid_select_label.setText(f"Обрано: {self.video_path}")
                self.btn_start.setEnabled(True)
                self.text_output.clear()

    def start_processing(self):
        if not self.video_path:
            QMessageBox.warning(self, "Увага", "Будь ласка, оберіть відеофайл!")
            return

        self.btn_start.setEnabled(False)
        self.vid_select_button.setEnabled(False)
        self.text_output.setText("Обробка відео... Будь ласка, зачекайте.")

        index = self.frames_to_skip_slider.value()
        frames_to_skip = self.frames_to_skip_values[index]
        self.worker = Worker(self.video_path, frames_to_skip)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, success, message):
        self.btn_start.setEnabled(True)
        self.vid_select_button.setEnabled(True)

        if success:
            try:
                with open("output.srt", "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_output.setText(content)
            except Exception as e:
                self.text_output.setText(f"Не вдалося відкрити output.srt: {str(e)}")
        else:
            self.text_output.setText(message)

        QMessageBox.information(self, "Статус", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubtitleExtractorApp()
    window.show()
    sys.exit(app.exec())
