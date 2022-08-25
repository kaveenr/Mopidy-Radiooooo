import Adafruit_SSD1306
from .constants import lookup_code

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class OLEDDisplay:

    def __init__(self, font):
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
        self.disp.begin()
        self.font = ImageFont.truetype(font, 18)
        self.font_small = ImageFont.truetype(font, 8)

    def clear(self):
        self.disp.clear()
        self.disp.display()

    def get_canvas(self):
        w, h = self.disp.width, self.disp.height
        image = Image.new('1', (w, h))
        draw = ImageDraw.Draw(image)
        return image, draw

    def set_canvas(self, image):
        self.disp.image(image)
        self.disp.display()

    def draw_country(self, code):
        w, h = self.disp.width, self.disp.height
        image, draw = self.get_canvas()
        draw.rectangle((0,0,w,h), outline=0, fill=0)
        
        txt = "Select Country"
        tw, th = draw.textsize(txt, font=self.font_small)
        draw.text(((w - tw)/2, -2), txt,  font=self.font_small, fill=255)

        txt = lookup_code(code)[0:11]
        tw, th = draw.textsize(txt, font=self.font)
        draw.text(((w - tw)/2, 8), txt,  font=self.font, fill=255)
        
        self.set_canvas(image)

    def draw_year(self, year):
        w, h = self.disp.width, self.disp.height
        image, draw = self.get_canvas()
        draw.rectangle((0,0,w,h), outline=0, fill=0)
        
        txt = "Select Year"
        tw, th = draw.textsize(txt, font=self.font_small)
        draw.text(((w - tw)/2, -2), txt,  font=self.font_small, fill=255)

        txt = f"{year}'s"
        tw, th = draw.textsize(txt, font=self.font)
        draw.text(((w - tw)/2, 8), txt,  font=self.font, fill=255)
        
        self.set_canvas(image)

item = OLEDDisplay('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
item.clear()
#item.draw_year(1980)
item.draw_country("LKA")