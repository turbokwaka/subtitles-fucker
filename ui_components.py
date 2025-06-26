# ui_components.py

from PyQt6.QtCore import QTimer, pyqtSlot
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QTextEdit, QComboBox, QPushButton, QSlider, QSizePolicy

from video_utils import load_and_show_frame, count_frames
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
import os

class DropWidget(QFrame):
    fileDropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.label = QLabel("Засади мені")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                self.label.setText(f"{os.path.basename(file_path)}")
                self.fileDropped.emit(file_path)
            event.acceptProposedAction()
        else:
            event.ignore()

class VideoFrameLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.original_pixmap = None
        self.x_0 = None
        self.x_1 = None
        self.y_0 = None
        self.y_1 = None
        self.selecting_frame:bool = False
        self.setFixedSize(640, 360)

        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.update_scaled_pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.selecting_frame:
                self.selecting_frame = True
                self.x_0 = event.pos().x()
                self.y_0 = event.pos().y()
                print(f"x_0={self.x_0}, y_0={self.y_0}")
            else:
                self.selecting_frame = False
                self.x_1 = event.pos().x()
                self.y_1 = event.pos().y()
                print(f"x_1={self.x_1}, y_1={self.y_1}")

    def update_scaled_pixmap(self):
        if self.original_pixmap:
            print(self.size().width(), self.size().height())
            scaled = self.original_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
            )
            self.setPixmap(scaled)
            print(self.size().width(), self.size().height())

class VideoSlider(QWidget):
    frame_selected = pyqtSignal(int)
    def __init__(self):
        super().__init__()

        self.frames_count = 0
        self._last_value = 0

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)

        self.frames_label = QLabel(f"{self._last_value} / {self.frames_count}")

        layout = QVBoxLayout()
        layout.addWidget(self.frames_label)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        self.slider.valueChanged.connect(self.on_slider_change)

        self._delay_timer = QTimer()
        self._delay_timer.setInterval(100)
        self._delay_timer.setSingleShot(True)
        self._delay_timer.timeout.connect(self.emit_delayed_signal)

    def set_max_frames(self, count: int):
        self.frames_count = count
        self.slider.setMaximum(count - 1)
        self.slider.setValue(0)

    def on_slider_change(self, value):
        self.frames_label.setText(f"{value} / {self.frames_count}")
        self._last_value = value
        self._delay_timer.start()

    def emit_delayed_signal(self):
        self.frame_selected.emit(self._last_value)

class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_frame_label = VideoFrameLabel()
        self.video_slider = VideoSlider()

        self.frames_count = None
        self.current_frame = None
        self.video_path = None

        self.video_slider.frame_selected.connect(self.on_frame_selected)

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_frame_label)
        layout.addWidget(self.video_slider)


    @pyqtSlot(str)
    def load_video(self, file_path):
        load_and_show_frame(file_path, self.video_frame_label)
        self.frames_count = count_frames(file_path)
        self.video_slider.set_max_frames(self.frames_count)
        self.video_path = file_path

    @pyqtSlot(int)
    def on_frame_selected(self, frame_number):
        if self.video_path is not None:
            load_and_show_frame(self.video_path, self.video_frame_label, frame_number)
            self.current_frame = frame_number

class SettingsItem(QWidget):
    def __init__(self, label_text: str, widget: QWidget, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(widget)

        self.setLayout(layout)

def create_main_widget(parent_window):
    central_widget = QWidget()
    main_layout = QHBoxLayout(central_widget)
    left_layout = QVBoxLayout()
    right_layout = QVBoxLayout()

    source_group = QGroupBox("Звідки субтитри витягуєм?")
    source_layout = QVBoxLayout(source_group)
    source_layout.addWidget(QLabel("🎬 Відеофайл:"))
    drop_widget = DropWidget()
    drop_widget.setObjectName("dropZone")
    source_layout.addWidget(drop_widget)

    text_edit = QTextEdit()
    source_layout.addWidget(QLabel("🔗 Посилання на відео?:"))
    text_edit.setPlaceholderText("Посилання на YouTube відео...")
    text_edit.setMaximumHeight(30)
    source_layout.addWidget(text_edit)
    left_layout.addWidget(source_group)

    settings_group = QGroupBox("⚙️ Налаштування")
    settings_layout = QVBoxLayout(settings_group)

    video_player = VideoPlayer()

    drop_widget.fileDropped.connect(video_player.load_video)
    settings_layout.addWidget(video_player)
    settings_layout.addStretch()

    select_lang = QComboBox()
    select_lang.addItem("Українська", "uk")
    select_lang.addItem("Англійська", "en")
    select_lang.addItem("Італійська", "it")
    select_lang.addItem("Японська", "jp")
    lang_setting = SettingsItem("Мова:", select_lang)

    select_frames_skip = QComboBox()
    select_frames_skip.addItem("1")
    select_frames_skip.addItem("15")
    select_frames_skip.addItem("30")
    select_frames_skip.addItem("45")
    select_frames_skip.addItem("60")
    frames_skip_setting = SettingsItem("Сіко кадрів пропускати?:", select_frames_skip)

    start_button = QPushButton("Погналі?")
    start_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    select_settings = QHBoxLayout()
    select_settings.addWidget(lang_setting)
    select_settings.addWidget(frames_skip_setting)
    select_settings.addStretch()
    select_settings.addWidget(start_button)
    settings_layout.addLayout(select_settings)

    left_layout.addWidget(settings_group, stretch=1)
    main_layout.addLayout(left_layout)

    return central_widget
