import settings
from PIL import Image, ImageDraw, ImageFont


class AsciiPictureGenerator:
    def __init__(self, size, width, height):
        self.picture_width = width
        self.picture_height = height
        self.font_size = size

    def generate_picture_art(self):
        with open(settings.save_path + 'art.txt', 'r') as f:
            text = f.read()
        font = ImageFont.truetype(r'fonts\lucida_console.ttf', 1 if self.font_size == 1 else self.font_size * 2 - 1)
        canvas = Image.new('RGB', (self.picture_width, self.picture_height), 'white')
        draw = ImageDraw.Draw(canvas)
        draw.text((0, 0), text, 'black', font, spacing=1)
        canvas.save(settings.save_path + "art-picture.png", "PNG")
