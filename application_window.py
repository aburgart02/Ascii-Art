import settings
import os.path
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QSlider, QLineEdit, QLabel, QFileDialog, QCheckBox
from PIL import Image
from ascii_art_generator import AsciiArtGenerator
from ascii_picture_generator import AsciiPictureGenerator
from progress_bar import ProgressBar
from settings import resolution_ratio


class ApplicationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)
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
        self.picture_size_hint_1 = QLabel('Неверный размер арта', self)
        self.picture_size_hint_2 = QLabel('Изображение не загружено', self)
        self.path = ''
        self.ascii_art = None
        self.ascii_picture = None
        self.progress_bar = None
        self.image = None
        self.pixmap = None
        self.set_background(1)
        self.configure_elements(1)
        self.hide_hints()
        self.assign_buttons()
        self.show()

    def keyPressEvent(self, e):
        if e.key() == 16777274:
            self.change_resolution()

    def change_resolution(self):
        if self.isFullScreen():
            self.showNormal()
            self.set_background(1)
            self.configure_elements(1)
        else:
            self.showFullScreen()
            self.set_background(resolution_ratio)
            self.configure_elements(resolution_ratio)
        if self.art_label.pixmap():
            self.configure_art()

    def hide_hints(self):
        self.picture_size_hint_1.hide()
        self.picture_size_hint_2.hide()

    def configure_elements(self, x):
        self.configure_buttons(x)
        self.configure_granularity_parameter(x)
        self.configure_size_parameters(x)
        self.configure_hints(x)

    def assign_buttons(self):
        self.generate_button.clicked.connect(self.generate_art)
        self.save_path_button.clicked.connect(self.change_save_path)
        self.remove_distortion_button.clicked.connect(self.remove_distortion)
        self.preserving_proportions_button.clicked.connect(self.keep_proportions)
        self.image_selection_button.clicked.connect(self.select_image)

    def set_background(self, x):
        self.background = self.background_image.scaled(QSize(1280 * x, 720 * x))
        self.palette.setBrush(QPalette.Window, QBrush(self.background))
        self.setPalette(self.palette)

    def select_image(self):
        self.path = QFileDialog.getOpenFileName()[0]
        if self.path == '':
            return
        self.image = Image.open(self.path)
        self.pixmap = QPixmap(self.path)
        if self.pixmap is None:
            self.picture_size_hint_2.show()
        else:
            self.picture_size_hint_2.hide()
        self.configure_art()

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
        if self.path == '':
            self.picture_size_hint_2.show()
            return
        else:
            if self.check_conditions(self.art_width, 0) and self.check_conditions(self.art_height, 1):
                self.picture_size_hint_1.hide()
                self.process_image(int(self.art_width.text()), int(self.art_height.text()),
                                   self.roberts_filter_checkbox.isChecked())
            else:
                self.picture_size_hint_1.show()

    def check_conditions(self, art_parameter, axis):
        try:
            return 1 <= int(art_parameter.text()) <= self.image.size[axis]
        except (ValueError, AttributeError):
            return False

    def process_image(self, width, height, roberts_filter_mode):
        self.progress_bar = ProgressBar(self, width, height)
        self.ascii_art = AsciiArtGenerator(self.path, width, height,
                                           roberts_filter_mode, int(self.granularity_level.value()), self.progress_bar)
        self.ascii_art.generate_text_art()
        self.ascii_picture = AsciiPictureGenerator(int(self.image.size[0] / width), self.image.size[0],
                                                   self.image.size[1])
        self.ascii_picture.generate_picture_art()
        self.pixmap = QPixmap(os.path.join(settings.save_path, 'art-picture.png'))
        self.configure_art()
        self.art_label.show()

    def configure_art(self):
        self.art_label.setStyleSheet('border-style: outset; border-width: 2px; border-color: blue;')
        if self.isFullScreen():
            self.art_label.setPixmap(self.pixmap.scaled(QSize(1080, 1080), Qt.KeepAspectRatio))
        else:
            self.art_label.setPixmap(self.pixmap.scaled(QSize(720, 720), Qt.KeepAspectRatio))
        self.art_label.adjustSize()
        self.art_label.move(0, (self.height() - self.art_label.height()) // 2)

    def configure_buttons(self, x):
        self.image_selection_button.setFixedSize(300 * x, 40 * x)
        self.image_selection_button.move(850 * x, 450 * x)
        self.image_selection_button.setStyleSheet('background-color: #570290; border-style: outset; border-width: 2px; '
                                                  'border-radius: 10px; border-color: blue; font: bold '
                                                  + str(int(20 * x)) +
                                                  'px; min-width: 0em; padding: 6px; color: white;')
        self.generate_button.setFixedSize(300 * x, 50 * x)
        self.generate_button.move(850 * x, 510 * x)
        self.generate_button.setStyleSheet('background-color: #570290; border-style: outset; border-width: 2px; '
                                           'border-radius: 10px; border-color: blue; font: bold ' + str(int(28 * x)) +
                                           'px; min-width: 0em; padding: 6px; color: white;')
        self.save_path_button.setIcon(QIcon(os.path.join("materials", "settings_picture.png")))
        self.save_path_button.setStyleSheet('background-color: rgb(0, 0, 0, 0)')
        self.save_path_button.setIconSize(QSize(80 * x, 80 * x))
        self.save_path_button.move(1160 * x, self.generate_button.y() - 20 * x)
        self.save_path_button.adjustSize()
        self.roberts_filter_checkbox.move(890 * x, 580 * x)
        self.roberts_filter_checkbox.setStyleSheet('background-color: #570290; border-style: outset; '
                                                   'border-width: 2px; border-radius: 0px; border-color: blue; '
                                                   'font: bold ' + str(int(20 * x)) + 'px; min-width: 0em; '
                                                                                      'padding: 6px; color: white;')
        self.roberts_filter_checkbox.adjustSize()
        self.remove_distortion_button.move(850 * x, 300 * x)
        self.remove_distortion_button.setStyleSheet('background-color: #570290; border-style: outset; '
                                                    'border-width: 2px; '
                                                    'border-radius: 10px; border-color: blue; font: bold '
                                                    + str(int(20 * x)) +
                                                    'px; min-width: 0em; padding: 6px; color: white;')
        self.remove_distortion_button.adjustSize()
        self.preserving_proportions_button.move(850 * x, 240 * x)
        self.preserving_proportions_button.setStyleSheet('background-color: #570290; border-style: outset; '
                                                         'border-width: 2px; '
                                                         'border-radius: 10px; border-color: blue; font: bold '
                                                         + str(int(20 * x)) +
                                                         'px; min-width: 0em; padding: 6px; color: white;')
        self.preserving_proportions_button.adjustSize()

    def configure_granularity_parameter(self, x):
        self.granularity_level_value.move(1120 * x, 390 * x)
        self.granularity_level_value.setStyleSheet('font-weight: 500; color: white; font-size:'
                                                   + str(int(20 * x)) + 'pt;')
        self.granularity_level_value.adjustSize()
        self.granularity_level_text.move(850 * x, 360 * x)
        self.granularity_level_text.setStyleSheet('font-weight: 500; color: white; font-size:' + str(12 * x) + 'pt;')
        self.granularity_level_text.adjustSize()
        self.granularity_level.setFixedSize(220 * x, 50 * x)
        self.granularity_level.move(850 * x, 390 * x)
        self.granularity_level.setTickPosition(QSlider.TicksBelow)
        self.granularity_level.setRange(1, 5)
        self.granularity_level.setStyleSheet("""
                            QSlider{
                            }
                            QSlider::groove:horizontal {  
                                height: 10px;
                                margin: 0px;
                                border-radius: 5px;
                                background: #B0AEB1;
                            }
                            QSlider::handle:horizontal {
                                background: #570290;
                                border: 1px solid #E3DEE2;
                                width: 17px;
                                margin: -5px 0; 
                                border-radius: 8px;
                            }
                            QSlider::sub-page:qlineargradient {
                                background: #0478C6;
                                border-radius: 5px;
                            }
                        """)
        self.granularity_level.valueChanged.connect(self.change_granularity_level)

    def configure_size_parameters(self, x):
        self.art_width_text.move(850 * x, 30 * x)
        self.art_width_text.setStyleSheet('font-weight: 500; color: white; font-size:' + str(14 * x) + 'pt;')
        self.art_width_text.adjustSize()
        self.art_height_text.move(850 * x, 130 * x)
        self.art_height_text.setStyleSheet('font-weight: 500; color: white; font-size:' + str(14 * x) + 'pt;')
        self.art_height_text.adjustSize()
        self.art_width.setFixedSize(300 * x, 50 * x)
        self.art_width.move(850 * x, 70 * x)
        self.art_width.setStyleSheet('background : #570290; font-weight: 500; color: white; font-size:' + str(18 * x)
                                     + 'pt; border: 2px solid blue; border-picture_width : 2px 2px 2px 2px;')
        self.art_width.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.art_height.setFixedSize(300 * x, 50 * x)
        self.art_height.move(850 * x, 170 * x)
        self.art_height.setStyleSheet('background : #570290; font-weight: 500; color: white; font-size:' + str(18 * x)
                                      + 'pt; border: 2px solid blue; border-picture_width : 2px 2px 2px 2px;')
        self.art_height.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def configure_hints(self, x):
        self.picture_size_hint_1.move(860 * x, 630 * x)
        self.picture_size_hint_1.setStyleSheet('font-weight: 500; color: white; font-size:' + str(14 * x) + 'pt;')
        self.picture_size_hint_1.adjustSize()
        self.picture_size_hint_2.move(860 * x, 630 * x)
        self.picture_size_hint_2.setStyleSheet('font-weight: 500; color: white; font-size:' + str(14 * x) + 'pt;')
        self.picture_size_hint_2.adjustSize()
