import glob
import os
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont

class Digitizer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.img = Image.open(filepath).convert("RGBA")
    def make_square(self, size=200):
        (w, h) = self.img.size
        if w > h: 
            x = (w - h) * 0.5
            y = 0
            box=(x, y, h + x, h + y)
        else:
            x = 0
            y = (h - w) * 0.5
            box=(x, y, x + w, y + w)
        self.img = self.img.resize((size, size), box=box)
        
    def adjust_contrast(self, amount=1.5):
        self.img = ImageEnhance.Contrast(self.img).enhance(amount)
    def make_grayscale(self):
        self.img = ImageOps.grayscale(self.img)
        self.img = self.img.convert("RGB")
    def add_watermark(self):
        font = ImageFont.truetype("ibm-plex-mono.ttf", 24)
        drawer = ImageDraw.Draw(self.img)
        drawer.text((32, 32), "SuperHi", font=font, fill=(255, 255, 255, 50))
    def convert_to_ascii(self):
        font_size = 10
        letters = [" ", ".", "!", "$", "&", "#"]
        (w, h) = self.img.size
        new_width = int(w / font_size)
        new_height = int(h / font_size)
        sample_size = (new_width, new_height)
        final_size = (new_width * font_size, new_height * font_size)
        self.make_grayscale()
        self.adjust_contrast(5.0)
        self.img = self.img.resize(sample_size)
        ascii_img = Image.new("RGBA", final_size, color="#000000")
        font = ImageFont.truetype("ibm-plex-mono.ttf", font_size)
        drawer = ImageDraw.Draw(ascii_img)
        for x in range(new_width):
            for y in range(new_height):
                (r, g, b) = self.img.getpixel((x, y))
                brightness = r / 256
                letter_num = int(len(letters) * brightness)
                letter = letters[letter_num]
                position = (x * font_size, y * font_size)
                drawer.text(position, letter, font=font, fill=(255, 255, 255, 255))
        self.img = ascii_img
    def save(self, output_filepath):
        if self.filepath.endswith(".jpg"):
            self.img = self.img.convert("RGB")
        self.img.save(output_filepath)

if __name__ == "__main__":
    inputs = glob.glob("inputs/*")
    inputs.sort()

    os.makedirs("outputs", exist_ok=True)

    for filepath in inputs:
        output = filepath.replace("inputs", "outputs")
        image = Digitizer(filepath)
        image.convert_to_ascii()
        image.save(output)

