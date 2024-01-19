# video_selector.py
import cv2
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QFileDialog, QSlider, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

class VideoSelector(QWidget):
    image_updated = pyqtSignal(QImage)
    def __init__(self, parent=None, main_widget=None):
        super(VideoSelector, self).__init__(parent)

        self.main_widget = main_widget  # Сохраняем указатель на главный виджет

        self.video_path = None
        self.slider_position = 0
        self.orig_frames = None


        layout = QVBoxLayout()

        self.label = QLabel(self)
        layout.addWidget(self.label)

        # self.slider = QSlider(Qt.Horizontal, self)
        # self.slider.sliderMoved.connect(self.set_slider_position)
        # layout.addWidget(self.slider)

        self.btn_select_video = QPushButton("Выбрать видео", self)
        self.btn_select_video.clicked.connect(self.select_video)
        layout.addWidget(self.btn_select_video)

        self.setLayout(layout)

    # def create_slider(self):
    #     slider = QSlider(Qt.Horizontal, self)
    #     slider.hide()  # Скрываем слайдер при создании
    #
    #
    #     # Если есть указатель на главный виджет, устанавливаем позицию слайдера относительно него
    #     if self.main_widget:
    #         widget_geometry = self.main_widget.geometry()
    #         slider.move(widget_geometry.width() // 2, widget_geometry.height() - 50)
    #
    #     return slider






    def select_video(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Videos (*.mp4 *.avi)")
        if file_dialog.exec_():
            self.video_path = file_dialog.selectedFiles()[0]
            self.play_video()



    def play_video(self, slider_position = 0):
        print('Видео проигрывается')
        print(f'Позиция слайдера: {slider_position}')
        if self.video_path:
            cap = cv2.VideoCapture(self.video_path)
            # cap.set(cv2.CAP_PROP_POS_FRAMES, self.slider_position)
            cap.set(cv2.CAP_PROP_POS_FRAMES, slider_position)
            ret, frame = cap.read()

            if ret:
                print('ret exs')
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)

                # Отправляем сигнал с изображением

                self.image_updated.emit(q_image)

                self.orig_frames = frame


                self.label.setPixmap(pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))

            # self.slider.setMaximum(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1)
            cap.release()

    # def get_selected_frame(self):
    #     if self.video_path:
    #         cap = cv2.VideoCapture(self.video_path)
    #         cap.set(cv2.CAP_PROP_POS_FRAMES, self.slider_position)
    #         ret, frame = cap.read()
    #         cap.release()
    #         return frame



if __name__ == "__main__":


    app = QApplication(sys.argv)
    window = VideoSelector()
    window.show()
    sys.exit(app.exec_())


