import math
import settings
import os.path
from settings import granularity_levels
from progress_bar import ProgressBar


class AsciiArtGenerator:
    def __init__(self, image, width, height, granularity_level, application_window):
        self.symbols = granularity_levels[granularity_level - 1]
        self.resized_image = image.resize((width, height), resample=0, box=None)
        self.progress_bar = ProgressBar(application_window, self.resized_image)

    def generate_text_art(self):
        with open(os.path.join(settings.save_path, 'art.txt'), 'w') as f:
            for height in range(0, self.resized_image.size[1]):
                for width in range(0, self.resized_image.size[0]):
                    self.progress_bar.value += 1
                    self.progress_bar.setValue(self.progress_bar.value)
                    average = sum([x for x in self.resized_image.getpixel((width, height))[:3]]) / 3
                    f.write(self.symbols[int(average) // math.ceil(255 / (len(self.symbols)))])
                f.write('\n')
        self.progress_bar.close()
