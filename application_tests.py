import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from application_window import ApplicationWindow
from progress_bar import ProgressBar


app = QApplication(sys.argv)
application = ApplicationWindow()
progress_bar_widget = ProgressBar(application, 100, 100)


class TestApplicationWindow:
    def test_application_window_size(self):
        assert application.size().width() == 1280 and application.size().height() == 720

    def test_background_loading(self):
        assert type(application.background) is QtGui.QImage

    def test_toggle_full_screen_on_off(self):
        application.change_resolution()
        assert application.isFullScreen()
        application.change_resolution()
        assert not application.isFullScreen()


class TestProgressBar:
    def test_maximum_value_setting(self):
        assert progress_bar_widget.maximum() == 10000
