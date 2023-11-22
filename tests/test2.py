import sys
import cv2
import tkinter as tk
from tkinter import filedialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QFileDialog, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore, QtGui


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.win_height = 1200
        self.win_width = 850
        self.import_image = None
        self.second_img = None

        self.init_ui()

    def init_ui(self):
        self.resize(self.win_width, self.win_height)
        self.add_widgets()
        # self.connect_events()

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()

        self.label_first.resize(w * 0.8, h * 0.3)
        self.label_second.resize(w * 0.8, h * 0.3)

        if self.pixmap_origin:
            self.label_first.setPixmap(self.pixmap_origin)
        if self.pixmap_gray:
            self.label_second.setPixmap(self.pixmap_gray)

    def add_widgets(self):

        self.btn_select_file = QPushButton('Выбрать файл', self)
        self.btn_select_file.move(0, 0)
        self.btn_select_file.setIcon(QtGui.QIcon('icons/select_file.png'))

        self.btn_gray = QPushButton('Преобразовать в серый', self)
        self.btn_gray.move(100, 0)
        self.btn_gray.setIcon(QtGui.QIcon('icons/edit.png'))

        self.label_first = QLabel(self)
        self.label_first.move(30, 100)
        self.label_first.resize(550, 300)
        self.label_first.setStyleSheet("background-color: rgb(43,43,43)")

        self.label_second = QLabel(self)
        self.label_second.move(30, 450)
        self.label_second.resize(550, 300)
        self.label_second.setStyleSheet("background-color: rgb(77,77,77)")

    def select_file(self):

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()

        if file_path:

            try:
                import_image = cv2.imread(file_path)

                if import_image is not None:

                    h, w = self.win_height / 2, self.win_width / 2
                    import_image = cv2.resize(import_image, (h, w))

                    height, width, channel = import_image.shape
                    bytesPerLine = 3 * width
                    qImg = QImage(import_image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

                    self.show_image_first(qImg)

                else:
                    print("Не удалось загрузить изображение.")

            except Exception as e:
                print(f"Ошибка при загрузке изображения: {str(e)}")

        else:
            print("Выбор файла отменен.")

    def show_image_first(self, img):

        self.pixmap_origin = QPixmap.fromImage(img)
        self.label_first.setPixmap(self.pixmap_origin)

    def img_to_gray(self):

        print('Преобразование в серый')

        second_img = cv2.cvtColor(self.import_image, cv2.COLOR_BGR2GRAY)

        h, w = self.win_height / 2, self.win_width / 2
        second_img = cv2.resize(second_img, (h, w))

        height, width = second_img.shape
        bytesPerLine = 3 * width
        qImg_gray = QImage(second_img.data, width, height, QImage.Format_Grayscale8)

        self.show_image_second(qImg_gray)

    def show_image_second(self, img):

        self.pixmap_gray = QPixmap.fromImage(img)
        self.label_second.setPixmap(self.pixmap_gray)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()