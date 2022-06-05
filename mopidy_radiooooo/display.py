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
    font = ImageFont.load_default()

    # Clear Out Bkg
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    draw.text((x, top),"Radiooooo",  font=font, fill=255)
    draw.text((x, top+8), state["year"], font=font, fill=255)
    draw.text((x, top+16), state["code"],  font=font, fill=255)

    disp.image(image)
    disp.display()
