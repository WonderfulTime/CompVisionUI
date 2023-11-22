import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import cv2


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(850, 1200)

        self.import_image = None
        self.second_img = None

        self.initUI()

    def initUI(self):

        self.btn_select = QPushButton('Select File', self)
        self.btn_select.move(0, 0)
        self.btn_select.clicked.connect(self.selectFile)

        self.btn_gray = QPushButton('To Gray', self)
        self.btn_gray.move(100, 0)
        self.btn_gray.clicked.connect(self.toGray)

        self.label_first = self.createFirstLabel()
        self.label_second = self.createSecondLabel()

        self.show()

    def createFirstLabel(self):

        label = QLabel(self)
        label.setStyleSheet("background-color: gray;")
        label.resize(550, 300)
        label.move(30, 100)

        return label

    def createSecondLabel(self):

        label = QLabel(self)
        label.setStyleSheet("background-color: gray;")
        label.resize(1100, 350)
        label.move(30, 450)

        return label

    def selectFile(self):
        # load image

        self.loadImage('example.jpg')

    def loadImage(self, filePath):

        img = cv2.imread(filePath)

        if img is not None:
            # convert to QImage
            h, w = img.shape[:2]
            qimage = QImage(img, w, h, QImage.Format_RGB888)

            # display in first label
            self.displayInLabel(qimage, self.label_first)

            # resize and convert to grayscale
            img = cv2.resize(img, (w // 2, h // 2))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # convert back to QImage
            qimage = QImage(gray.data, w // 2, h // 2, QImage.Format_Grayscale8)

            # display in second label
            self.displayInLabel(qimage, self.label_second)

    def displayInLabel(self, qimage, label):
        pixmap = QPixmap.fromImage(qimage)
        label.setPixmap(pixmap)

    def toGray(self):

        if self.import_image is not None:
            img = self.import_image.copy()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            h, w = gray.shape[:2]
            qimage = QImage(gray, w, h, QImage.Format_Grayscale8)

            self.displayInLabel(qimage, self.label_second)

    def resizeEvent(self, event):

        w = event.size().width()
        h = event.size().height()

        # resize first label
        self.label_first.resize(w * 0.5, h * 0.25)

        # resize pixmap inside
        pixmap = self.label_first.pixmap()
        pixmap = pixmap.scaled(self.label_first.width(), self.label_first.height(), Qt.KeepAspectRatio)
        self.label_first.setPixmap(pixmap)

        # resize second label
        self.label_second.resize(w * 0.5, h * 0.25)
        self.label_second.move(w * 0.5, h * 0.5)

        pixmap = self.label_second.pixmap()
        pixmap = pixmap.scaled(self.label_second.width(), self.label_second.height(), Qt.KeepAspectRatio)
        self.label_second.setPixmap(pixmap)


app = QApplication(sys.argv)

window = MainWindow()
app.exec()