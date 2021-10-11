import os.path
import settings
from PyQt5 import QtGui
from application_window import ApplicationWindow
from ascii_art_generator import AsciiArtGenerator
from ascii_picture_generator import AsciiPictureGenerator
from progress_bar import ProgressBar

application = ApplicationWindow()
progress_bar_widget = ProgressBar(application, 100, 100)
art_generator = AsciiArtGenerator(os.path.join('pictures', 'photo_1.jpg'), 100, 100, False)
art_generator.generate_text_art()
picture_generator = AsciiPictureGenerator(1, 100, 100)


class TestApplicationWindow:
    def test_application_window_size(self):
        assert application.size().width() == 1280 and application.size().height() == 720

    def test_background_loading(self):
        assert type(application.background) is QtGui.QImage

    def test_toggle_full_screen_on(self):
        application.change_resolution()
        assert application.isFullScreen()

    def test_toggle_full_screen_off(self):
        application.change_resolution()
        assert not application.isFullScreen()


class TestProgressBar:
    def test_maximum_value_setting(self):
        assert progress_bar_widget.maximum() == 10000


class TestAsciiArtGenerator:
    def test_art_generation(self):
        with open(os.path.join('art.txt'), 'r') as f:
            art = f.read()
        assert art_generator.resized_image.size[0] * art_generator.resized_image.size[1] == len(art) \
               - art_generator.resized_image.size[1]

    def test_art_width(self):
        with open(os.path.join('art.txt'), 'r') as f:
            art = f.readline()
        assert art_generator.resized_image.size[0] == len(art) - 1

    def test_art_height(self):
        count = 0
        with open(os.path.join('art.txt'), 'r') as f:
            while True:
                count += 1
                line = f.readline()
                if not line:
                    break
        assert art_generator.resized_image.size[1] == count - 1

    def test_allowed_symbols_in_art(self):
        result = True
        with open(os.path.join('art.txt'), 'r') as f:
            art = f.read()
        for symbol in art:
            if symbol not in settings.granularity_levels[0] and symbol != '\n':
                result = False
        assert result is True

    def test_png_image_format(self):
        generator = AsciiArtGenerator(os.path.join('pictures', 'photo_5.png'), 60, 40, False)
        generator.generate_text_art()
        with open(os.path.join('art.txt'), 'r') as f:
            art = f.read()
        assert len(art) != 0

    def test_granularity_level_selection(self):
        generator = AsciiArtGenerator(os.path.join('pictures', 'photo_5.png'), 60, 40, False, 2)
        assert generator.symbols == settings.granularity_levels[1]


class TestAsciiPictureGenerator:
    def test_picture_generation(self):
        picture_generator.generate_picture_art()
        with open(os.path.join('art-picture.png'), 'r') as f:
            assert f is not None
