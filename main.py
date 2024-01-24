from video_selector import VideoSelector
from screen_capturing import ScreenCapture
# from settings import SettingsDialog
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

import numpy as np




# дочерний класс, наследующийся от QWidget
# Класс QWidget в PyQt представляет базовый класс для всех виджетов (окон, кнопок, полей и т.д.).
class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # использование композиция для решения проблемы порядка наследования возникающей из-за того, что несколько раз наследуется от QWidget
        self.video_selector = VideoSelector()

        # класс скриншота
        self.screen_capturing = ScreenCapture()

        # передача изображения из класса VideoSelector
        self.video_selector.image_updated.connect(self.show_image_first)
        # self.video_selector = VideoSelector(main_widget=self)
        self.Video_img = False

        self.display_rule = "intensity"  # начальное правило - интенсивность


        self.win_height = 1200
        self.win_width = 850
        self.import_image = None
        self.second_img = None
        # self.resizeEvent(self.resizeEvent)

        self.slider_position = 0


        self.init_ui()
        # self.show()

    # стандартные параметры для окна
    def init_ui(self):
        # self.setFixedSize(self.win_height, self.win_width)
        self.add_widgets()
        self.connect_events()
        self.create_slider()

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
        self.comboBox_files.addItem('Видео')
        self.comboBox_files.addItem('Скриншот')
        self.comboBox_files.addItem('Изображение')
        self.comboBox_files.move(0, 0)

        # иконка комбобокса
        self.comboBox_files.setStyleSheet('QComboBox::down-arrow { image: url(icons/select_file_icon.png); }')

        # вызов действия кнопки при активации ее внутри вып списка
        self.comboBox_files.activated.connect(self.perform_action_on_select)



        self.btn_change_img_to_gray = self.create_button("Цвет/полутон", self.img_to_gray)
        self.btn_change_img_to_gray.move(100, 0)
        self.btn_change_img_to_gray.setIcon(QtGui.QIcon('icons/edit_icon.png'))



        # комбобокс для настроек
        # Добавляем кнопку "Настройки"
        self.comboBox_settings = QComboBox(self)
        self.comboBox_settings.addItem('Настройка преобразования в полутон')  # PlaceHolder
        self.comboBox_settings.addItem("Интенсивность")
        self.comboBox_settings.addItem("Яркость")
        self.comboBox_settings.addItem("Красный")
        self.comboBox_settings.addItem("Зеленый")
        self.comboBox_settings.addItem("Синий")

        self.comboBox_settings.move(210, 0)
        self.comboBox_settings.activated.connect(self.activation_settings_comboBox)





        self.label_select_first = self.create_label_first()
        self.label_select_second = self.create_label_second()








    # функция при активации комбобокса "Файл"
    def perform_action_on_select(self):
        # Функция, которая будет вызываться при выборе элемента в выпадающем списке
        selected_action = self.comboBox_files.currentText()
        if selected_action == 'Изображение':
            print('Выполнено Изображение')
            self.hide_slider()
            self.Video_img = False
            self.select_file()

        elif selected_action == 'Видео':
            # cur_lab_pos = self.label.pos()
            # new_xpos_slider, new_ypos_slider = cur_lab_pos.x(), cur_lab_pos.y() хз как брать координаты от label
            new_xpos_slider = 30
            new_ypos_slider = 400 + 10


            self.slider.move(new_xpos_slider, new_ypos_slider)
            # сброс позиции слайдера на 0
            self.slider.setValue(0)
            self.show_slider()

            # доп проверка для преобр кадров видео
            self.Video_img = True
            self.video_selector.select_video()
            print('Выполнено Видео')

        elif selected_action == 'Скриншот':
            print('Делаем скрин')
            # посылаем в модуль для скринов размеры мэйн окна для корректировки изображений
            taken_screenshot, original_screen_img = self.screen_capturing.msgBox(self.win_height, self.win_width)
            self.import_image = original_screen_img
            self.Video_img = False
            print('отпр данные в show_image_first')
            self.show_image_first(taken_screenshot)




        else:
            print('Выберите действие')


    # функция при активации комбобокса настроек
    def activation_settings_comboBox(self):
        selected_action = self.comboBox_settings.currentText()

        if selected_action == "Интенсивность":
            self.display_rule = "intensity"

        elif selected_action == "Яркость":
            self.display_rule = "brightness"

        elif selected_action == "Красный":
            self.display_rule = "red"

        elif selected_action == "Зеленый":
            self.display_rule = "green"

        elif selected_action == "Синий":
            self.display_rule = "blue"

        print(self.display_rule)




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
        # при попытке перевода в серый вылет, скорее всего из-за кодировки изображения (fixed)
        if self.Video_img == True:
            self.q_image = img


        img_label = self.create_label_first()
        # img_label.resize(img.width(), img.height())
        # хранимое изображение
        pixmap_origin = QPixmap.fromImage(img)
        img_label.setPixmap(pixmap_origin)
        print("Отобразил img")
        # self.pixmap_origin = pixmap_origin


    def rule_for_second_img(self, rgb_image):


        # дефолтное определение значения
        gray_image = (rgb_image[:, :, 0] + rgb_image[:, :, 1] + rgb_image[:, :, 2]) // 3

        if self.display_rule == "intensity":
            gray_image = (rgb_image[:, :, 0] + rgb_image[:, :, 1] + rgb_image[:, :, 2]) // 3
        elif self.display_rule == "brightness":
            gray_image = (0.299 * rgb_image[:, :, 0] + 0.587 * rgb_image[:, :, 1] + 0.114 * rgb_image[:, :, 2]).astype(
                np.uint8)

        elif self.display_rule == "red":
            print(f"Processing 'red'. Shape of rgb_image: {rgb_image.shape}")
            gray_image = rgb_image[:, :, 0]
            print(f"Processed 'red'. Shape of gray_image: {gray_image.shape}")

        elif self.display_rule == "green":
            print(f"Shape of rgb_image[:, :, 1]: {rgb_image[:, :, 1].shape}")
            gray_image = rgb_image[:, :, 1]
        elif self.display_rule == "blue":
            print(f"Shape of rgb_image[:, :, 2]: {rgb_image[:, :, 2].shape}")
            gray_image = rgb_image[:, :, 2]

        return gray_image



    # конверт изображения в серый
    def img_to_gray(self):
        # скорее всего условия неверно поставлены
        if self.import_image is not None:
            import_image = self.import_image

        elif self.Video_img == True:
            print('кадры')

            # тырим фрейм изображения из класс VideoSelector
            import_image = self.video_selector.orig_frames

        # elif

        # если изображение не выбрано
        else:
            print('Нет изображения')
            return


        print(f'self.Video_img = {self.Video_img}')
        print('Процесс преобразования в серый')
        origin_img = import_image
        # second_img = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY)

        try:

            h, w = int(self.win_height / 2), int(self.win_width / 2)
            second_img = cv2.resize(origin_img, (h, w))

        except Exception as e:
            print(e)

        # вызов правила преобразования
        second_img = self.rule_for_second_img(second_img)

        # print(self.second_img)
        height, width = second_img.shape
        print(f"x={height} y={width}")
        bytesPerLine = 3 * width
        # переменная содержащая изображение
        try:
            data_bytes = bytes(second_img)
            qImg_gray = QImage(data_bytes, width, height, QImage.Format_Grayscale8)
        except Exception as e:
            print(e)

        # отрисовка серого (монохромного) изображения
        print('qImg_gray')
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

    def create_slider(self):
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.hide()  # Скрываем слайдер при создании
        self.slider.setFixedWidth(300)
        self.slider.sliderMoved.connect(self.set_slider_position)


        return self.slider

    # скрытие слайдера
    def hide_slider(self):
        self.slider.hide()

    # показ слайдера
    def show_slider(self):
        self.slider.show()

    def set_slider_position(self, position):

        self.slider_position = position
        self.video_selector.play_video(self.slider_position)





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


