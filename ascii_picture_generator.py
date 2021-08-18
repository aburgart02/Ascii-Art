from PIL import Image, ImageDraw, ImageFont
from settings import font_size


class AsciiPictureGenerator:
    def __init__(self, scale_level, picture_width, picture_height):
        self.width = picture_width
        self.height = picture_height
        self.scale = scale_level

    def generate_picture_art(self):
        with open('art.txt', 'r') as f:
            text = f.read()
        font = ImageFont.truetype(r'fonts\lucida_console.ttf', font_size[self.scale])
        canvas = Image.new('RGB', (self.width, self.height), 'white')
        draw = ImageDraw.Draw(canvas)
        draw.text((0, 0), text, 'black', font, spacing=1)
        canvas.save("art-picture.png", "PNG")
