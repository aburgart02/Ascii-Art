import math
import settings
import os.path
import click
from PIL import Image
from settings import granularity_levels


class AsciiArtGenerator:
    def __init__(self, path, width, height, roberts_filter_mode, granularity_level=None, progress_bar=None):
        self.image = Image.open(path)
        self.symbols = granularity_levels[granularity_level - 1] if granularity_level is not None \
            else ['@', '#', 'S', '%', '?', '*', '+', ':', ',', '.', ' ']
        self.resized_image = self.image.resize((width, height), resample=0, box=None)
        if roberts_filter_mode:
            self.resized_image = self.roberts_cross(self.resized_image)
        self.progress_bar = progress_bar

    def generate_text_art(self):
        with open(os.path.join(settings.save_path, 'art.txt'), 'w') as f:
            for height in range(0, self.resized_image.size[1]):
                for width in range(0, self.resized_image.size[0]):
                    if self.progress_bar is not None:
                        self.progress_bar.value += 1
                        self.progress_bar.setValue(self.progress_bar.value)
                    average = sum([x for x in self.resized_image.getpixel((width, height))[:3]]) / 3
                    f.write(self.symbols[int(average) // math.ceil(255 / (len(self.symbols)))])
                f.write('\n')
        if self.progress_bar is not None:
            self.progress_bar.close()

    @staticmethod
    def roberts_cross(image):
        for width in range(0, image.size[0] - 1):
            for height in range(0, image.size[1] - 1):
                z1 = sum(image.getpixel((width, height))[:3]) / 3
                z2 = sum(image.getpixel((width + 1, height + 1))[:3]) / 3
                z3 = sum(image.getpixel((width + 1, height))[:3]) / 3
                z4 = sum(image.getpixel((width, height + 1))[:3]) / 3
                g1, g2 = z1 - z2, z3 - z4
                result = 255 - int(math.sqrt(g1 * g1 + g2 * g2))
                image.putpixel((width, height), (result, result, result))
        return image


@click.command()
@click.argument('path')
@click.argument('width')
@click.argument('height')
@click.argument('roberts_filter_mode')
def generate_art(path, width, height, roberts_filter_mode):
    if roberts_filter_mode == 'on':
        ascii_art_generator = AsciiArtGenerator(path, int(width), int(height), True)
        ascii_art_generator.generate_text_art()
    if roberts_filter_mode == 'off':
        ascii_art_generator = AsciiArtGenerator(path, int(width), int(height), False)
        ascii_art_generator.generate_text_art()


if __name__ == '__main__':
    generate_art()
