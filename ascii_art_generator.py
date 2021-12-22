import math
import settings
import os.path
import click
from PIL import Image
from settings import granularity_levels


class AsciiArtGenerator:
    def __init__(self, granularity_level=None, progress_bar=None):
        self.symbols = granularity_levels[granularity_level - 1] if granularity_level is not None \
            else ['@', '#', 'S', '%', '?', '*', '+', ':', ',', '.', ' ']
        self.progress_bar = progress_bar

    def generate_text_art(self, path, width, height, roberts_filter_mode, save_path=None):
        image = Image.open(path)
        resized_image = image.resize((width, height), resample=0, box=None)
        if roberts_filter_mode:
            resized_image = self.roberts_cross(resized_image)
        save_path = os.path.join(settings.save_path, 'art.txt') if save_path is None else save_path
        with open(save_path, 'w') as f:
            for height in range(0, resized_image.size[1]):
                for width in range(0, resized_image.size[0]):
                    if self.progress_bar is not None:
                        self.progress_bar.value += 1
                        self.progress_bar.setValue(self.progress_bar.value)
                    average = sum([x for x in resized_image.getpixel((width, height))[:3]]) / 3
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
@click.option('-ip', required=True, help='Image path')
@click.option('-sp', default='art.txt', help='Save path')
@click.option('-m', default='off', type=click.Choice(['on', 'off']), help='Image processing mode')
@click.option('-w', default=150, help='Art width')
@click.option('-h', default=100, help='Art height')
def generate_art(ip, sp, m, w, h):
    ascii_art_generator = AsciiArtGenerator()
    try:
        if m == 'on':
            ascii_art_generator.generate_text_art(ip, int(w), int(h), True, sp)
        if m == 'off':
            ascii_art_generator.generate_text_art(ip, int(w), int(h), False, sp)
    except Exception as e:
        raise click.ClickException(str(e))


if __name__ == '__main__':
    generate_art()
