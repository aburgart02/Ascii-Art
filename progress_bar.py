from PyQt5.QtWidgets import QProgressBar
from settings import resolution_ratio


class ProgressBar(QProgressBar):
    def __init__(self, application_window, image, scale):
        super().__init__(application_window)
        self.setMaximum((image.size[0] - scale) * (int(image.size[1] * (2 / 3)) - scale))
        self.value = 0
        if application_window.isFullScreen():
            self.setFixedSize(320 * resolution_ratio, 40 * resolution_ratio)
            self.setStyleSheet('color: white; font-size: ' + str(int(20 * resolution_ratio)) + 'px')
            self.move(850 * resolution_ratio, 570 * resolution_ratio)
        else:
            self.setFixedSize(320, 40)
            self.setStyleSheet('color: white; font-size: 20px')
            self.move(850, 570)
        self.show()
