import sys
import PIL
import math
import settings
import os.path
import click
from PIL import Image
from settings import granularity_levels


class AsciiArtGenerator:
    def __init__(self, path, width, height, roberts_filter_mode, granularity_level=None,
                 progress_bar=None, save_path=None):
        self.image = self.load_image(path)
        self.symbols = granularity_levels[granularity_level - 1] if granularity_level is not None \
            else ['@', '#', 'S', '%', '?', '*', '+', ':', ',', '.', ' ']
        self.resized_image = self.image.resize((width, height), resample=0, box=None)
        if roberts_filter_mode:
            self.resized_image = self.roberts_cross(self.resized_image)
        self.progress_bar = progress_bar
        self.save_path = os.path.join(settings.save_path, 'art.txt') if save_path is None else save_path

    def generate_text_art(self):
        with open(self.save_path, 'w') as f:
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

    @staticmethod
    def load_image(path):
        sys.tracebacklimit = 0
        try:
            return Image.open(path)
        except PIL.UnidentifiedImageError as e:
            raise e
        except FileNotFoundError as e:
            raise e
        except FileExistsError as e:
            raise e


@click.command()
@click.option('-ip', required=True, help='Image path')
@click.option('-sp', default='art.txt', help='Save path')
@click.option('-m', default='off', type=click.Choice(['on', 'off']), help='Image processing mode')
@click.option('-w', default=150, help='Art width')
@click.option('-h', default=100, help='Art height')
def generate_art(ip, sp, m, w, h):
    if m == 'on':
        ascii_art_generator = AsciiArtGenerator(ip, int(w), int(h), True, None, None, sp)
        ascii_art_generator.generate_text_art()
    if m == 'off':
        ascii_art_generator = AsciiArtGenerator(ip, int(w), int(h), False, None, None, sp)
        ascii_art_generator.generate_text_art()


if __name__ == '__main__':
    generate_art()
