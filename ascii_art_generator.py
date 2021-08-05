from PIL import Image


class AsciiArtGenerator:
    def __init__(self, path, scale_level):
        self.image = Image.open(path)
        self.symbols = ['@', '#', 'S', '%', '?', '*', '+', ':', ',', '.', ' ']
        self.scale = scale_level
        self.resized_image = self.image.resize((self.image.size[0], int(self.image.size[1]
                                                                        * (2 / 3))), resample=0, box=None)

    def generate_text_art(self):
        with open('art.txt', 'w') as f:
            for height in range(0, self.resized_image.size[1] - self.scale, self.scale):
                for width in range(0, self.resized_image.size[0] - self.scale, self.scale):
                    average = 0
                    for block_height in range(0, self.scale):
                        for block_width in range(0, self.scale):
                            for part in range(0, 3):
                                average += (self.resized_image.getpixel((width + block_height,
                                                                         height + block_width))[part]
                                            / (3 * self.scale ** 2))
                    f.write(self.symbols[int(average) // 25])
                f.write('\n')
