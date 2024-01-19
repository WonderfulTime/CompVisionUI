import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog, QSlider, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialog



class ImageVideoProcessor(QMainWindow):
    def __init__(self):
        super(ImageVideoProcessor, self).__init__()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.mode_button = QPushButton('Цвет/Полутон', self)
        self.mode_button.clicked.connect(self.toggle_display_mode)

        self.settings_button = QPushButton('Настройки', self)
        self.settings_button.clicked.connect(self.show_settings)

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.mode_button)
        self.layout.addWidget(self.settings_button)

        self.display_mode = "color"  # "color" or "grayscale"

        self.crop_button = QPushButton('Кадрирование', self)
        self.crop_button.clicked.connect(self.crop_image)
        self.layout.addWidget(self.crop_button)

        self.screen_capture_button = QPushButton('Захват экрана', self)
        self.screen_capture_button.clicked.connect(self.capture_screen)
        self.layout.addWidget(self.screen_capture_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_frame)
        self.frame_interval = 500
        self.num_frames = 20

        self.create_settings_dialog()

    def toggle_display_mode(self):
        self.display_mode = "grayscale" if self.display_mode == "color" else "color"
        self.show_image()

    def show_image(self):
        if self.image is not None:
            if self.display_mode == "color":
                image = self.image.copy()
            else:
                image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)

    def load_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "",
                                                   "Image Files (*.png *.jpg *.bmp);;Video Files (*.mp4 *.avi);;All Files (*)",
                                                   options=options)

        if file_name:
            self.image = cv2.imread(file_name)
            self.show_image()

    def create_settings_dialog(self):
        self.settings_dialog = QDialog(self)
        self.settings_dialog.setWindowTitle('Настройки')
        self.settings_dialog.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout(self.settings_dialog)

        self.frames_slider = QSlider(Qt.Horizontal, self.settings_dialog)
        self.frames_slider.setMinimum(1)
        self.frames_slider.setMaximum(50)
        self.frames_slider.setValue(self.num_frames)
        self.frames_slider.valueChanged.connect(self.update_num_frames)

        self.interval_slider = QSlider(Qt.Horizontal, self.settings_dialog)
        self.interval_slider.setMinimum(100)
        self.interval_slider.setMaximum(2000)
        self.interval_slider.setValue(self.frame_interval)
        self.interval_slider.valueChanged.connect(self.update_frame_interval)

        layout.addWidget(QLabel('Количество кадров для видео:'))
        layout.addWidget(self.frames_slider)
        layout.addWidget(QLabel('Интервал между кадрами (мс):'))
        layout.addWidget(self.interval_slider)

        self.settings_dialog.hide()

    def update_num_frames(self):
        self.num_frames = self.frames_slider.value()

    def update_frame_interval(self):
        self.frame_interval = self.interval_slider.value()

    def show_settings(self):
        self.settings_dialog.show()

    def crop_image(self):
        # Implement image cropping logic here
        pass

    def capture_screen(self):
        self.timer.start(self.frame_interval)
        QApplication.setOverrideCursor(Qt.CrossCursor)
        QApplication.instance().aboutToQuit.connect(self.release_screen_capture)

    def show_next_frame(self):
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, 0, 0, screen.size().width(), screen.size().height())
        screenshot.save("screen_capture.png", "png")
        self.image = cv2.imread("screen_capture.png")
        self.show_image()

    def release_screen_capture(self):
        self.timer.stop()
        QApplication.restoreOverrideCursor()


def main():
    app = QApplication(sys.argv)
    window = ImageVideoProcessor()
    window.setWindowTitle('IVP - Обработка изображений и видео')
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
