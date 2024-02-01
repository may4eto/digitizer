from js import document, console, window
from pyodide import create_proxy
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps

def adjust_contrast(img, amount=1.5):
    img = ImageEnhance.Contrast(img).enhance(amount)
    
def make_grayscale(img):
    img = ImageOps.grayscale(img)
    img = img.convert("RGB")

def convert_to_ascii():
    image = window.getElementById("output_upload").firstElementChild
    font_size = 10
    letters = [" ", ".", "!", "$", "&", "#"]
    (w, h) = image.size
    new_width = int(w / font_size)
    new_height = int(h / font_size)
    sample_size = (new_width, new_height)
    final_size = (new_width * font_size, new_height * font_size)
    make_grayscale(image)
    adjust_contrast(image, 5.0)
    image = image.resize(sample_size)
    ascii_img = Image.new("RGBA", final_size, color="#000000")
    font = ImageFont.truetype("ibm-plex-mono.ttf", font_size)
    drawer = ImageDraw.Draw(ascii_img)
    for x in range(new_width):
        for y in range(new_height):
            (r, g, b) = image.getpixel((x, y))
            brightness = r / 256
            letter_num = int(len(letters) * brightness)
            letter = letters[letter_num]
            position = (x * font_size, y * font_size)
            drawer.text(position, letter, font=font, fill=(255, 255, 255, 255))
    image = ascii_img
    document.getElementById("output_upload").appendChild(image)

transform_file = create_proxy(convert_to_ascii)

document.getElementById("file-transform").addEventListener("click", transform_file)