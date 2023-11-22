
import cv2
import tkinter as tk
from tkinter import filedialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QFileDialog, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


# перенес код из main'а, на всякий

# дочерний класс, наследующийся от QWidget
# Класс QWidget в PyQt представляет базовый класс для всех виджетов (окон, кнопок, полей и т.д.).
class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.win_height = 1200
        self.win_width = 850
        self.import_image = None
        self.second_img = None
        # self.resizeEvent(self.resizeEvent)

        self.init_ui()
        # self.show()

    # стандартные параметры для окна
    def init_ui(self):
        # self.setFixedSize(self.win_height, self.win_width)
        self.add_widgets()
        self.connect_events()

    # тут обновляются виджеты при изменении размера окна
    def resizeEvent(self, event):
        self.create_label_first()
        self.create_label_second()

    # self.button.move(self.width() * 0.1, self.height() * 0.1)

    # виджеты
    def add_widgets(self):




        # создание кнопок в выпадающем списке
        self.comboBox_files = QComboBox(self)
        self.comboBox_files.addItem('Файл') # PlaceHolder
        self.comboBox_files.addItem('Действие 1')
        self.comboBox_files.addItem('Действие 2')
        self.comboBox_files.addItem('Изображение')
        self.comboBox_files.move(0, 0)

        # иконка комбобоксу
        self.comboBox_files.setStyleSheet('QComboBox::down-arrow { image: url(icons/select_file_icon.png); }')


        # # НЕ РАБОТАЕТ WIP
        # # Флаг для отслеживания того, был ли выбор сделан
        # self.selection_comboBox_files_made = False
        # # Подключаем событие currentIndexChanged для скрытия/отображения плейсхолдера
        # self.comboBox_files.currentIndexChanged.connect(self.handle_index_change)
        # # Подключаем событие showPopup к выпадающему списку (когда список открывается)
        # self.comboBox_files.view().focusInEvent = self.handle_show_event




        # вызов действия кнопки при активации ее внутри вып списка
        self.comboBox_files.activated.connect(self.perform_action_on_select)



        # Кнопка перенесена в комбобокс
        # self.btn_select_new_file = self.create_button("Изображение", self.select_file)
        # self.btn_select_new_file.move(0, 0)
        # self.btn_select_new_file.setIcon(QtGui.QIcon('icons/select_file_icon.png'))
        # self.comboBox_files.addItem(self.btn_select_new_file.text())

        self.btn_change_img_to_gray = self.create_button("Изображение в серый", self.img_to_gray)
        self.btn_change_img_to_gray.move(100, 0)
        self.btn_change_img_to_gray.setIcon(QtGui.QIcon('icons/edit_icon.png'))

        self.label_select_first = self.create_label_first()
        self.label_select_second = self.create_label_second()



    # # не работает WIP
    # # При открытии выпадающего списка обновляем флаг и плейсхолдер
    # def handle_show_event(self, event):
    #     print('aa')
    #     self.selection_comboBox_files_made = False
    #     self.comboBox_files.setPlaceholderText('Файл')
    #     self.comboBox_files.view().showEvent = None  # После первого открытия убираем обработчик, чтобы не мешал дальше
    #
    # # не работает WIP
    # # Показываем/скрываем плейсхолдер в зависимости от того, был ли выбор сделан
    # def handle_index_change(self, index):
    #     print('zalupa')
    #
    #     if self.selection_comboBox_files_made:
    #         self.comboBox_files.setPlaceholderText('')
    #     else:
    #         self.selection_comboBox_files_made = True



    # функция при активации комбобокса
    def perform_action_on_select(self):
        # Функция, которая будет вызываться при выборе элемента в выпадающем списке
        selected_action = self.comboBox_files.currentText()
        if selected_action == 'Изображение':
            print('Выполнено Изображение')
            self.select_file()
        elif selected_action == 'Действие 1':
            print('Выполнено Действие 1')
        elif selected_action == 'Действие 2':
            print('Выполнено Действие 2')
        else:
            print('Выберите действие')



    # создание общего стиля отступа для объектов
    def create_label_first(self):
        label = QLabel(self)
        label.setScaledContents(True)
        label.move(30, 100)

        label.resize(550, 300)
        label.setStyleSheet("background-color:  rgb(43,43,43)")

        label.show()
        return label

    def create_label_second(self):
        label_second = QLabel(self)
        label_second.setScaledContents(True)
        label_second.move(30, 450)
        label_second.resize(1100, 350)
        label_second.setStyleSheet("background-color:  rgb(77,77,77)")

        label_second.show()
        return label_second

    def create_button(self, text, callback):
        btn = QPushButton(text, self)
        btn.clicked.connect(callback)
        return btn

    def select_file(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()

        print(file_path)

        if file_path:
            try:
                import_image = cv2.imread(file_path)
                if import_image is not None:

                    # изменение размеров изображение под размер окна
                    h, w = int(self.win_height / 2), int(self.win_width / 2)
                    self.import_image = cv2.resize(import_image, (h, w))

                    height, width, channel = self.import_image.shape
                    print(f"x={height} y={width}")
                    bytesPerLine = 3 * width
                    # переменная содержащая изображение
                    qImg = QImage(self.import_image.data, width, height, bytesPerLine,
                                  QImage.Format_RGB888).rgbSwapped()
                    # self.show_image(qImg, width, height) пока не использую
                    # вызов функции с отрисовкой изображения
                    self.show_image_first(qImg)



                else:
                    print("Не удалось загрузить изображение.")

            # разобраться с варнингом при кириллице
            # [ WARN:0@4.151] global loadsave.cpp:248 cv::findDecoder imread_('C:/Users/User/Desktop/польз данные/ключ.JPG'): can't open/read file: check file path/integrity
            except RuntimeWarning as wrong_name:
                print(f"Кириллица в имени {str(wrong_name)}")
            except Exception as e:
                print(f"Произошла ошибка при загрузке изображения: {str(e)}")
        else:
            print("Выбор файла был отменен.")

    # показ оригинального изображения
    def show_image_first(self, img):
        img_label = self.create_label_first()
        # img_label.resize(img.width(), img.height())
        # хранимое изображение
        pixmap_origin = QPixmap.fromImage(img)
        img_label.setPixmap(pixmap_origin)
        print("Отобразил img")
        # self.pixmap_origin = pixmap_origin

    # конверт изображения в серый
    def img_to_gray(self):
        print('Процесс преобразования в серый')
        origin_img = self.import_image
        second_img = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY)

        h, w = int(self.win_height / 2), int(self.win_width / 2)
        self.second_img = cv2.resize(second_img, (h, w))
        # print(self.second_img)
        height, width = self.second_img.shape
        print(f"x={height} y={width}")
        bytesPerLine = 3 * width
        # переменная содержащая изображение
        qImg_gray = QImage(self.second_img.data, width, height, QImage.Format_Grayscale8)
        # отрисовка серого изображения
        self.show_image_second(qImg_gray)

    def show_image_second(self, img):
        # отображение измененного изображения
        print('Процесс отображения серого')
        img_label = self.create_label_second()
        # img_label.resize(img.width(), img.height())
        # хранимое изображение
        pixmap_second = QPixmap.fromImage(img)
        img_label.setPixmap(pixmap_second)
        print("Отобразил img_gray")

    def connect_events(self):
        ...

    def keyPressEvent(self, event):
        # если нажата клавиша F11
        if event.key() == QtCore.Qt.Key_F11:
            # если в полный экран
            if self.isFullScreen():
                # вернуть прежнее состояние
                self.showNormal()
            else:
                # иначе во весь экран
                self.showFullScreen()

    # вызывается при любом изменении размера окна
    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        print(w, h)






# класс инициализации приложения
class App(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.window = MainWindow()
        self.window.show()
        # exec - бесконечный обработчик событий
        self.exec()


if __name__ == '__main__':
    app = App(sys.argv)


