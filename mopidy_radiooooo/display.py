import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def draw_data(disp, state):
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    draw = ImageDraw.Draw(image)

    draw.rectangle((0,0,width,height), outline=0, fill=0)

    padding = -2
    top = padding
    bottom = height-padding
    x = 0


    # Clear Out Bkg
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
    font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 8)

    tw, th = draw.textsize(state["code"], font=font_small)
    draw.text(((width - tw)/2, top), state["code"],  font=font_small, fill=255)

    tw, th = draw.textsize(state["year"], font=font)
    draw.text(((width - tw)/2, top+8), state["year"],  font=font, fill=255)

    disp.image(image)
    disp.display()
