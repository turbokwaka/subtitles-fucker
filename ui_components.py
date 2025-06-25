# ui_components.py

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QTextEdit

from main_window import load_and_show_first_frame

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
    video_label = VideoFrameLabel()
    video_label.setObjectName("frameSelect")

    drop_widget.fileDropped.connect(lambda path: load_and_show_first_frame(path, video_label))
    settings_layout.addWidget(video_label, alignment=Qt.AlignmentFlag.AlignCenter)

    left_layout.addWidget(settings_group, stretch=1)
    main_layout.addLayout(left_layout)

    return central_widget
