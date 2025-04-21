import os
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QMovie
from PyQt5.QtCore import Qt, QTimer
import imageio.v2 as iio

class TransparentVisionOverlay(QWidget):
    def __init__(self, animation_frames, fps=10):
        super().__init__()
        self.animation_frames = animation_frames
        self.current_frame = 0
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // fps)    # Adjust for your desired FPS
# class TransparentVisionOverlay(QWidget):
#     def __init__(self, apng_path, flags=Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool):
#         super().__init__(flags=flags)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.label = QLabel(self)
#         self.movie = QMovie(apng_path)
#         self.movie.setCacheMode(QMovie.CacheAll)
#         self.label.setMovie(self.movie)
#         self.movie.start()
        
    def initUI(self):
        # Set window flags for a frameless, always-on-top, transparent window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 200, 300)

        self.layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.layout.addWidget(self.label)

    def update_frame(self):
        if self.animation_frames is None:
            raise ValueError("Animation frames are null")
        if self.current_frame < 0 or self.current_frame >= len(self.animation_frames):
            raise ValueError("Current frame is out of range")
        frame = self.animation_frames[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

        # Use NumPy's buffer interface to avoid copying the data
        if frame is None:
            raise ValueError("Current frame is null")
        self.label.setPixmap(QPixmap.fromImage(QImage(
            frame.data, frame.shape[1], frame.shape[0], frame.strides[0],
            QImage.Format_RGBA8888 if frame.shape[2] == 4 else QImage.Format_RGB888)))

    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    # Load images from folder
    image_folder = 'transparent_frames(40)'     # Path to your folder with images!
    images = []
    for img_name in os.listdir(image_folder):
        if img_name.endswith('.png'):
            img_path = os.path.join(image_folder, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)  # Load with alpha channel
            if img is not None:
                # Convert BGR to RGBA if it's a color image
                if img.shape[2] == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
                elif img.shape[2] == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
                images.append(img)
                
    # def save_apng(frames, fps, path="animation.apng"):
    #     with iio.get_writer(path, mode="I", fps=fps) as writer:
    #         for f in frames:
    #             writer.append_data(f)   # frame must stay RGBA uint8
    #     print(f"Saved {path}")
        
    fps = 10
    

    app = QApplication(sys.argv)
    # window = TransparentVisionOverlay("animation.apng")

    # save_apng(images, fps)
    window = TransparentVisionOverlay(images, fps)
    window.show()
    sys.exit(app.exec())