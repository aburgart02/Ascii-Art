from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QSlider, QLineEdit, QLabel, QFileDialog
from ascii_art_generator import AsciiArtGenerator
from ascii_picture_generator import AsciiPictureGenerator


class ApplicationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)
        self.background_file = r"backgrounds\background.jpg"
        self.image = QImage(self.background_file)
        self.background = self.image.scaled(QSize(1280, 720))
        self.palette = QPalette()
        self.generate_button = QPushButton('Обработать', self)
        self.generate_button.clicked.connect(self.generate_art)
        self.granularity_level = QSlider(Qt.Horizontal, self)
        self.granularity_level_value = QLabel('1', self)
        self.granularity_level_text = QLabel('Выберите уровень детализации:', self)
        self.art_label = QLabel(self)
        self.scale = QLineEdit(self)
        self.scale_text = QLabel('Выберите масштаб:', self)
        self.path = ''
        self.ascii_art = None
        self.ascii_picture = None
        self.pixmap = None
        self.set_background(1)
        self.configure_elements(1)
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
            self.set_background(1.5)
            self.configure_elements(1.5)
        if self.art_label.pixmap():
            self.configure_art()

    def configure_elements(self, x):
        self.granularity_level_value.move(1120 * x, 300 * x)
        self.granularity_level_value.setStyleSheet('font-weight: 500; color: white; font-size:' + str(int(20 * x)) + 'pt;')
        self.granularity_level_value.adjustSize()
        self.granularity_level_text.move(850 * x, 250 * x)
        self.granularity_level_text.setStyleSheet('font-weight: 500; color: white; font-size:' + str(14 * x) + 'pt;')
        self.granularity_level_text.adjustSize()
        self.generate_button.setFixedSize(300 * x, 50 * x)
        self.generate_button.move(850 * x, 500 * x)
        self.generate_button.setStyleSheet('background-color: #570290; border-style: outset; border-width: 2px; '
                                           'border-radius: 10px; border-color: blue; font: bold ' + str(int(28 * x)) +
                                           'px; min-width: 0em; padding: 6px; color: white;')
        self.granularity_level.setFixedSize(220 * x, 50 * x)
        self.granularity_level.move(850 * x, 300 * x)
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
        self.scale_text.move(850 * x, 50 * x)
        self.scale_text.setStyleSheet('font-weight: 500; color: white; font-size:' + str(14 * x) + 'pt;')
        self.scale_text.adjustSize()
        self.scale.setFixedSize(300 * x, 50 * x)
        self.scale.move(850 * x, 100 * x)
        self.scale.setStyleSheet('background : #570290; font-weight: 500; color: white; font-size:' + str(18 * x)
                                 + 'pt; border: 2px solid blue; border-width : 2px 2px 2px 2px;')
        self.scale.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def set_background(self, x):
        self.background = self.image.scaled(QSize(1280 * x, 720 * x))
        self.palette.setBrush(QPalette.Window, QBrush(self.background))
        self.setPalette(self.palette)

    def change_granularity_level(self):
        self.granularity_level_value.setText(str(self.granularity_level.value()))

    def generate_art(self):
        if self.scale.text() == '':
            return
        self.path = QFileDialog.getOpenFileName()[0]
        if self.path == '':
            return
        self.ascii_art = AsciiArtGenerator(self.path, int(self.scale.text()), int(self.granularity_level.value()))
        self.ascii_art.generate_text_art()
        self.ascii_picture = AsciiPictureGenerator(int(self.scale.text()), self.ascii_art.image.size[0],
                                                   self.ascii_art.image.size[1])
        self.ascii_picture.generate_picture_art()
        self.art_label.setStyleSheet('border-style: outset; border-width: 2px; border-color: blue;')
        self.pixmap = QPixmap('art-picture.png')
        self.configure_art()
        self.art_label.show()

    def configure_art(self):
        if self.isFullScreen():
            self.art_label.setPixmap(self.pixmap.scaled(QSize(1080, 1080), Qt.KeepAspectRatio))
        else:
            self.art_label.setPixmap(self.pixmap.scaled(QSize(720, 720), Qt.KeepAspectRatio))
        self.art_label.adjustSize()
        self.art_label.move(0, (self.height() - self.art_label.height()) // 2)
