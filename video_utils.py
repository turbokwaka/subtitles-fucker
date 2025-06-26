# video_utils.py

import cv2
from PyQt6.QtGui import QImage, QPixmap

def frame_to_pixmap(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (640, 360), interpolation=cv2.INTER_AREA)
    h, w, ch = resized.shape
    bytes_per_line = ch * w
    image = QImage(resized.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(image)

def load_and_show_frame(video_path, label_widget, frame_number=1024):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    success, frame = cap.read()
    cap.release()
    if success:
        pixmap = frame_to_pixmap(frame)
        label_widget.setPixmap(pixmap)
        label_widget.original_pixmap = pixmap

def count_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total

def get_video_wh(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Не вдалося відкрити відео: {video_path}")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise ValueError("Не вдалося прочитати кадр з відео")

    height, width = frame.shape[:2]
    return width, height
