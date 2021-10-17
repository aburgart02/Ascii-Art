from PyQt5.QtWidgets import QProgressBar


class ProgressBar(QProgressBar):
    def __init__(self, application_window, width, height):
        super().__init__(application_window)
        self.setMaximum(width * height)
        self.value = 0
        if application_window.isFullScreen():
            self.setFixedSize(360 * application_window.resolution_ratio, 40 * application_window.resolution_ratio)
            self.setStyleSheet('color: white; font-size: ' + str(int(20 * application_window.resolution_ratio)) + 'px')
            self.move(850 * application_window.resolution_ratio, 640 * application_window.resolution_ratio)
        else:
            self.setFixedSize(360, 40)
            self.setStyleSheet('color: white; font-size: 20px')
            self.move(850, 640)
        self.show()
