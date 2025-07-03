import os

from PyQt6.QtCore import pyqtSignal, QThread
from videocr import get_subtitles


class TranscribeWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, video_path, frames_to_skip, lang, crop_x, crop_y, crop_width, crop_height):
        super().__init__()
        self.video_path = video_path
        self.frames_to_skip = frames_to_skip
        self.lang = lang
        self.crop_x = crop_x
        self.crop_y = crop_y
        self.crop_width = crop_height
        self.crop_height = crop_width

    def run(self):
        try:
            # перевіряєм чи вже існує output.srt
            # якщо так - видаляєм йо нахуй))
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(script_dir, "output.srt")
            if os.path.exists(output_path):
                os.remove(output_path)
                print("output.srt було знайдено і знищено.")
            print(f"Using parameters:\n"
                  f"frames_to_skip: {self.frames_to_skip}\n"
                  f"lang: {self.lang}\n"
                  f"crop_x: {self.crop_y}\n"
                  f"crop_y: {self.crop_x}\n"
                  f"crop_width: {self.crop_width}\n"
                  f"crop_height: {self.crop_height}\n")
            output = get_subtitles(video_path=self.video_path,
                                   frames_to_skip=self.frames_to_skip,
                                   lang=self.lang,
                                   crop_x=self.crop_y,
                                   crop_y=self.crop_x,
                                   crop_width=self.crop_width,
                                   crop_height=self.crop_height,
                                   use_gpu=True
                                   )
            self.finished.emit(True, output)
        except Exception as e:
            self.finished.emit(False, f"Помилка: {str(e)}")