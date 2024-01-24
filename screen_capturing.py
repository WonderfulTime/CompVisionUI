import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QPixmap, QImage
import pyautogui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import cv2

# типа msgbox'а для пользователя с вводом координат
class ScreenCaptureDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label_start_x = QLabel('Начало X:')
        self.edit_start_x = QLineEdit(self)
        layout.addWidget(label_start_x)
        layout.addWidget(self.edit_start_x)

        label_start_y = QLabel('Начало Y:')
        self.edit_start_y = QLineEdit(self)
        layout.addWidget(label_start_y)
        layout.addWidget(self.edit_start_y)

        label_end_x = QLabel('Конец X:')
        self.edit_end_x = QLineEdit(self)
        layout.addWidget(label_end_x)
        layout.addWidget(self.edit_end_x)

        label_end_y = QLabel('Конец Y:')
        self.edit_end_y = QLineEdit(self)
        layout.addWidget(label_end_y)
        layout.addWidget(self.edit_end_y)

        btn_capture = QPushButton('Capture', self)
        btn_capture.clicked.connect(self.capture)
        layout.addWidget(btn_capture)

        self.setLayout(layout)
        self.setWindowTitle("Скриншот")

    def capture(self):
        try:
            self.start_x = int(self.edit_start_x.text())
            self.start_y = int(self.edit_start_y.text())
            self.end_x = int(self.edit_end_x.text())
            self.end_y = int(self.edit_end_y.text())



            self.accept()  # Закрываем диалог только если введены корректные значения
        except ValueError:
            print("Invalid input. Please enter valid integers.")





    # делаем скрин области
    def screen_capture(self, start_x, start_y, end_x, end_y):
        try:
            screenshot = pyautogui.screenshot(region=(start_x, start_y, end_x - start_x,
                                                      end_y - start_y))

            screenshot.save("screens/screenshot.png")

            pixmap_orig = cv2.imread("screens/screenshot.png")

            # pixmap = screenshot.scaled(400, 300, Qt.KeepAspectRatio)
            #
            # preview_label = QLabel(self)
            # preview_label.setPixmap(pixmap)
            # preview_label.show()

            return pixmap_orig

        except Exception as e:
            print(e)



class ScreenCapture(QWidget):
    def __init__(self):
        super().__init__()

    # показ диалогового окна с выбором координат
    def msgBox(self, win_height = 100, win_width = 100):
        dialog = ScreenCaptureDialog()
        if dialog.exec_() == QDialog.Accepted:


            # отправляем координаты и делаем скрин
            result_screenshot = dialog.screen_capture(dialog.start_x, dialog.start_y, dialog.end_x, dialog.end_y)

            # сейв оригинала для дальнейшего
            orig_img = result_screenshot

            # изменение размеров изображение под размер окна
            h, w = int(win_height / 2), int(win_width / 2)
            result_screenshot = cv2.resize(result_screenshot, (h, w))

            height, width, channel = result_screenshot.shape
            print(f"x={height} y={width}")
            bytesPerLine = 3 * width

            result_screenshot = QImage(result_screenshot.data, width, height, bytesPerLine,
                                  QImage.Format_RGB888).rgbSwapped()

            print("Сделан скрин с координатами:",
                  dialog.start_x, dialog.start_y, dialog.end_x, dialog.end_y)

            # print(result_screenshot)

            return result_screenshot, orig_img


        else:
            print('Скрин не сделан')