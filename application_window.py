import PIL
import settings
import os.path
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QSlider, QLineEdit, QLabel, QFileDialog, QCheckBox, QDesktopWidget
from PIL import Image
from ascii_art_generator import AsciiArtGenerator
from ascii_picture_generator import AsciiPictureGenerator
from progress_bar import ProgressBar

F11_KEY = 16777274


class ApplicationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)
        self.resolution_ratio = QDesktopWidget().availableGeometry().width() / 1280
        self.background_file = os.path.join("backgrounds", "background.jpg")
        self.background_image = QImage(self.background_file)
        self.background = self.background_image.scaled(QSize(1280, 720))
        self.palette = QPalette()
        self.generate_button = QPushButton('Обработать', self)
        self.image_selection_button = QPushButton('Загрузите изображение', self)
        self.save_path_button = QPushButton(self)
        self.roberts_filter_checkbox = QCheckBox('Фильтр Робертса', self)
        self.remove_distortion_button = QPushButton('Исправить искажение по оси Y', self)
        self.preserving_proportions_button = QPushButton('Сохранить пропорции', self)
        self.granularity_level = QSlider(Qt.Horizontal, self)
        self.granularity_level_value = QLabel('1', self)
        self.granularity_level_text = QLabel('Выберите уровень детализации:', self)
        self.art_label = QLabel(self)
        self.art_width = QLineEdit(self)
        self.art_height = QLineEdit(self)
        self.art_width_text = QLabel('Введите ширину:', self)
        self.art_height_text = QLabel('Введите высоту:', self)
        self.picture_size_hint = QLabel(self)
        self.path = ''
        self.ascii_art = None
        self.ascii_picture = None
        self.progress_bar = None
        self.image = None
        self.pixmap = None
        self.set_background(1)
        self.configure_elements(1)
        self.assign_buttons()
        self.show()

    def keyPressEvent(self, e):
        if e.key() == F11_KEY:
            self.change_resolution()

    def change_resolution(self):
        if self.isFullScreen():
            self.showNormal()
            self.set_background(1)
            self.configure_elements(1)
        else:
            self.showFullScreen()
            self.set_background(self.resolution_ratio)
            self.configure_elements(self.resolution_ratio)
        if self.art_label.pixmap():
            self.configure_art()

    def configure_elements(self, x):
        self.configure_buttons(x)
        self.configure_granularity_parameter(x)
        self.configure_size_parameters(x)
        self.configure_hint(x)

    def assign_buttons(self):
        self.generate_button.clicked.connect(self.generate_art)
        self.save_path_button.clicked.connect(self.change_save_path)
        self.remove_distortion_button.clicked.connect(self.remove_distortion)
        self.preserving_proportions_button.clicked.connect(self.keep_proportions)
        self.image_selection_button.clicked.connect(self.select_image)

    def set_background(self, x):
        self.background = self.background_image.scaled(QSize(int(1280 * x), int(720 * x)))
        self.palette.setBrush(QPalette.Window, QBrush(self.background))
        self.setPalette(self.palette)

    def set_hint(self, text):
        self.picture_size_hint.setText(text)
        self.picture_size_hint.adjustSize()
        self.picture_size_hint.show()

    def select_image(self):
        self.path = QFileDialog.getOpenFileName(filter="Images (*.png *.jpg *bmp)")[0]
        if self.path == '':
            return
        self.pixmap = QPixmap(self.path)
        if self.pixmap is None:
            self.set_hint('Изображение не загружено')
        else:
            self.picture_size_hint.hide()
        self.image = self.load_image()
        self.configure_art()

    def load_image(self):
        try:
            return Image.open(self.path)
        except PIL.UnidentifiedImageError:
            self.set_hint('Неверный формат файла')
        except FileNotFoundError:
            self.set_hint('Файл не найден')
        except FileExistsError:
            self.set_hint('Файл не существует')

    def change_granularity_level(self):
        self.granularity_level_value.setText(str(self.granularity_level.value()))

    def remove_distortion(self):
        if self.check_conditions(self.art_height, 1):
            self.art_height.setText(str(int(int(self.art_height.text()) * (2 / 3))))

    def keep_proportions(self):
        if self.check_conditions(self.art_width, 0):
            self.art_height.setText(str(int(self.image.size[1] / (self.image.size[0] / int(self.art_width.text())))))

    @staticmethod
    def change_save_path():
        settings.save_path = QFileDialog.getExistingDirectory()

    def generate_art(self):
        if self.image is None:
            self.set_hint('Изображение не загружено')
            return
        else:
            if self.check_conditions(self.art_width, 0) and self.check_conditions(self.art_height, 1):
                self.picture_size_hint.hide()
                self.process_image(int(self.art_width.text()), int(self.art_height.text()),
                                   self.roberts_filter_checkbox.isChecked())
            else:
                self.set_hint('Неверный размер арта')

    def check_conditions(self, art_parameter, axis):
        try:
            return 1 <= int(art_parameter.text()) <= self.image.size[axis]
        except (ValueError, AttributeError):
            return False

    def process_image(self, width, height, roberts_filter_mode):
        self.progress_bar = ProgressBar(self, width, height)
        self.ascii_art = AsciiArtGenerator(int(self.granularity_level.value()), self.progress_bar)
        self.ascii_art.generate_text_art(self.path, width, height, roberts_filter_mode)
        self.ascii_picture = AsciiPictureGenerator(int(self.image.size[0] / width), self.image.size[0],
                                                   self.image.size[1])
        self.ascii_picture.generate_picture_art()
        self.pixmap = QPixmap(os.path.join(settings.save_path, 'art-picture.png'))
        self.configure_art()
        self.art_label.show()

    def configure_art(self):
        self.art_label.setStyleSheet(settings.art_label_style)
        if self.isFullScreen():
            self.art_label.setPixmap(self.pixmap.scaled(QSize(1080, 1080), Qt.KeepAspectRatio))
        else:
            self.art_label.setPixmap(self.pixmap.scaled(QSize(720, 720), Qt.KeepAspectRatio))
        self.art_label.adjustSize()
        self.art_label.move(0, (self.height() - self.art_label.height()) // 2)

    def configure_buttons(self, x):
        self.image_selection_button.setFixedSize(int(300 * x), int(40 * x))
        self.image_selection_button.move(int(850 * x), int(450 * x))
        self.image_selection_button.setStyleSheet(settings.button_style.format(str(int(20 * x))))
        self.generate_button.setFixedSize(int(300 * x), int(50 * x))
        self.generate_button.move(int(850 * x), int(510 * x))
        self.generate_button.setStyleSheet(settings.button_style.format(str(int(28 * x))))
        self.save_path_button.setIcon(QIcon(os.path.join("materials", "settings_picture.png")))
        self.save_path_button.setStyleSheet('background-color: rgb(0, 0, 0, 0)')
        self.save_path_button.setIconSize(QSize(int(80 * x), int(80 * x)))
        self.save_path_button.move(int(1160 * x), int(self.generate_button.y() - 20 * x))
        self.save_path_button.adjustSize()
        self.roberts_filter_checkbox.move(int(890 * x), int(580 * x))
        self.roberts_filter_checkbox.setStyleSheet(settings.roberts_filter_checkbox_style.format(str(int(20 * x))))
        self.roberts_filter_checkbox.adjustSize()
        self.remove_distortion_button.move(int(850 * x), int(300 * x))
        self.remove_distortion_button.setStyleSheet(settings.button_style.format(str(int(20 * x))))
        self.remove_distortion_button.adjustSize()
        self.preserving_proportions_button.move(int(850 * x), int(240 * x))
        self.preserving_proportions_button.setStyleSheet(settings.button_style.format(str(int(20 * x))))
        self.preserving_proportions_button.adjustSize()

    def configure_granularity_parameter(self, x):
        self.granularity_level_value.move(int(1120 * x), int(390 * x))
        self.granularity_level_value.setStyleSheet(settings.text_style.format(str(int(20 * x))))
        self.granularity_level_value.adjustSize()
        self.granularity_level_text.move(int(850 * x), int(360 * x))
        self.granularity_level_text.setStyleSheet(settings.text_style.format(str(12 * x)))
        self.granularity_level_text.adjustSize()
        self.granularity_level.setFixedSize(int(220 * x), int(50 * x))
        self.granularity_level.move(int(850 * x), int(390 * x))
        self.granularity_level.setTickPosition(QSlider.TicksBelow)
        self.granularity_level.setRange(1, 5)
        self.granularity_level.setStyleSheet(settings.slider_style)
        self.granularity_level.valueChanged.connect(self.change_granularity_level)

    def configure_size_parameters(self, x):
        self.art_width_text.move(int(850 * x), int(30 * x))
        self.art_width_text.setStyleSheet(settings.text_style.format(str(14 * x)))
        self.art_width_text.adjustSize()
        self.art_height_text.move(int(850 * x), int(130 * x))
        self.art_height_text.setStyleSheet(settings.text_style.format(str(14 * x)))
        self.art_height_text.adjustSize()
        self.art_width.setFixedSize(int(300 * x), int(50 * x))
        self.art_width.move(int(850 * x), int(70 * x))
        self.art_width.setStyleSheet(settings.size_input_fields_style.format(str(18 * x)))
        self.art_width.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.art_height.setFixedSize(int(300 * x), int(50 * x))
        self.art_height.move(int(850 * x), int(170 * x))
        self.art_height.setStyleSheet(settings.size_input_fields_style.format(str(18 * x)))
        self.art_height.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def configure_hint(self, x):
        self.picture_size_hint.move(int(860 * x), int(630 * x))
        self.picture_size_hint.setStyleSheet(settings.text_style.format(str(14 * x)))
        self.picture_size_hint.adjustSize()
