# ui_components.py

from PyQt6.QtCore import QTimer, pyqtSlot, QRect
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QTextEdit, QComboBox, QPushButton, QSlider, QSizePolicy

from video_utils import load_and_show_frame, count_frames, get_video_wh
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
    region_selected = pyqtSignal(int, int, int, int)
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.original_pixmap = None
        self.setFixedSize(640, 360)
        self.setObjectName("frameSelect")

        self.selecting = False
        self.start_point = None
        self.end_point = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selecting = True
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if self.selecting:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.selecting:
            self.selecting = False
            self.end_point = event.pos()
            self.update()
            x0, y0 = self.start_point.x(), self.start_point.y()
            x1, y1 = self.end_point.x(), self.end_point.y()

            print(f"Selected rectangle: ({x0}, {y0}) -> ({x1}, {y1})")
            self.region_selected.emit(x0, y0, x1, y1)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.start_point and self.end_point and (self.selecting or self.start_point != self.end_point):
            painter = QPainter(self)
            pen = QPen(QColor("#4cc9f0"), 2, Qt.PenStyle.DashLine)
            painter.setPen(pen)
            rect = QRect(self.start_point, self.end_point)
            painter.drawRect(rect)


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

        # Центрування відео лейбла
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(self.video_frame_label)
        h_layout.addStretch(1)

        self.frames_count = None
        self.current_frame = None
        self.video_path = None
        self.video_width = None
        self.video_height = None

        self.video_slider.frame_selected.connect(self.on_frame_selected)
        self.video_frame_label.region_selected.connect(self.handle_region_selected)

        layout = QVBoxLayout(self)
        layout.addLayout(h_layout)
        layout.addWidget(self.video_slider)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


    @pyqtSlot(str)
    def load_video(self, file_path):
        load_and_show_frame(file_path, self.video_frame_label)
        self.frames_count = count_frames(file_path)
        self.video_slider.set_max_frames(self.frames_count)
        self.video_width, self.video_height = get_video_wh(file_path)
        self.video_path = file_path

    @pyqtSlot(int)
    def on_frame_selected(self, frame_number):
        if self.video_path is not None:
            load_and_show_frame(self.video_path, self.video_frame_label, frame_number)
            self.current_frame = frame_number

    @pyqtSlot(int, int, int, int)
    def handle_region_selected(self, x0, y0, x1, y1):
        x_min, y_min, x_max, y_max = self.translate_wh(x0, y0, x1, y1)
        print(f"Selected video coords: ({x_min}, {y_min}) -> ({x_max}, {y_max})")

    def translate_wh(self, x0, y0, x1, y1):
        if None in (self.video_width, self.video_height):
            print("⛔️ Відео не завантажено, або розміри ще не встановлені.")
            return 0, 0, 0, 0

        widget_width = self.video_frame_label.width()
        widget_height = self.video_frame_label.height()

        nx0 = x0 / widget_width
        ny0 = y0 / widget_height
        nx1 = x1 / widget_width
        ny1 = y1 / widget_height

        vx0 = int(nx0 * self.video_width)
        vy0 = int(ny0 * self.video_height)
        vx1 = int(nx1 * self.video_width)
        vy1 = int(ny1 * self.video_height)

        x_min, x_max = sorted([vx0, vx1])
        y_min, y_max = sorted([vy0, vy1])

        return x_min, y_min, x_max, y_max


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
    parent_window.drop_widget = DropWidget()
    parent_window.drop_widget.setObjectName("dropZone")
    source_layout.addWidget(parent_window.drop_widget)

    parent_window.text_edit = QTextEdit()
    source_layout.addWidget(QLabel("🔗 Посилання на відео?:"))
    parent_window.text_edit.setPlaceholderText("Посилання на YouTube відео...")
    parent_window.text_edit.setMaximumHeight(30)
    source_layout.addWidget(parent_window.text_edit)
    left_layout.addWidget(source_group)

    settings_group = QGroupBox("⚙️ Налаштування")
    settings_layout = QVBoxLayout(settings_group)

    parent_window.video_player = VideoPlayer()
    parent_window.video_path = None
    parent_window.crop_rect = None

    parent_window.video_player.video_frame_label.region_selected.connect(
        lambda x0, y0, x1, y1: setattr(
            parent_window,
            "crop_rect",
            parent_window.video_player.translate_wh(x0, y0, x1, y1)
        )
    )
    parent_window.drop_widget.fileDropped.connect(parent_window.video_player.load_video)
    settings_layout.addWidget(parent_window.video_player)
    settings_layout.addStretch()

    parent_window.select_lang = QComboBox()
    parent_window.select_lang.addItem("Українська", "uk")
    parent_window.select_lang.addItem("Англійська", "en")
    parent_window.select_lang.addItem("Італійська", "it")
    parent_window.select_lang.addItem("Японська", "jp")
    lang_setting = SettingsItem("Мова:", parent_window.select_lang)

    parent_window.select_frames_skip = QComboBox()
    parent_window.select_frames_skip.addItems(["1", "15", "30", "45", "60"])
    frames_skip_setting = SettingsItem("Скіко кадрів пропускати?:", parent_window.select_frames_skip)

    parent_window.start_button = QPushButton("Погналі?")
    parent_window.start_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
    parent_window.start_button.clicked.connect(parent_window.start_transcription)

    select_settings = QHBoxLayout()
    select_settings.addWidget(lang_setting)
    select_settings.addWidget(frames_skip_setting)
    select_settings.addStretch()
    select_settings.addWidget(parent_window.start_button)
    settings_layout.addLayout(select_settings)

    left_layout.addWidget(settings_group, stretch=1)
    main_layout.addLayout(left_layout)

    return central_widget

