import os

from PyQt6.QtCore import pyqtSignal, QThread
from videocr import save_subtitles_to_file


class TranscribeWorker(QThread):
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