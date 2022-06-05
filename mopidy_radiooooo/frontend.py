import pykka, time
from mopidy import core

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO

# Pin Config
RST = None

butt_conf = {
    10: "year_up",
    9: "year_down",
    17: "code_up",
    27: "code_down"
}

from .display import draw_data


def increment_opt(increment, options, idx):
    n_idx = idx + 1 if increment else idx - 1
    if n_idx < 0:
        n_idx = len(options) -1
    elif n_idx >= len(options):
        n_idx = 0
    return n_idx

class RadioooooFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(RadioooooFrontend, self).__init__()
        self.core = core
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
        self.disp.clear()
        self.disp.display()
        # Frontend State
        self.year_options = [ str(1900 + (i*10)) for i in range(0,12)]
        self.code_options = [ "LKA", "AGO", "RUS", "CHN", "JPN", "THA"]
        self.year_index = 8
        self.code_index = 0
        self.warm_down = 4
        # Setup Buttons
        GPIO.setmode(GPIO.BCM)
        for pin, code in butt_conf.items():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(pin, GPIO.RISING, callback=self.on_button_press, bouncetime=300)

    def on_start(self):
        self.update_display()
        while True:
            self.warm_down = 0 if self.warm_down == 0 else self.warm_down - 1
            if self.warm_down == 0:
                channel = f"radiooooo:{self.year_options[self.year_index]}:{self.code_options[self.code_index]}"
                print(f"Playing Now {channel}")
                self.warm_down = -1
                self.core.playback.stop()
                self.core.tracklist.clear()
                self.core.tracklist.add(uris=[channel])
                self.core.playback.play()
            time.sleep(1)

    def on_stop(self):
        self.disp.clear()
        self.disp.display()

    def update_display(self):
        draw_data(self.disp, {
            "code": self.code_options[self.code_index],
            "year": self.year_options[self.year_index]
        })
    
    def on_button_press(self, channel):
        current = butt_conf[channel]
        print(f"Whoa {butt_conf[channel]} was clicked")
        if current == "year_up":
            self.year_index = increment_opt(True, self.year_options, self.year_index)
        elif current == "year_down":
            self.year_index = increment_opt(False, self.year_options, self.year_index)
        if current == "code_up":
            self.code_index = increment_opt(True, self.code_options, self.code_index)
        elif current == "code_down":
            self.code_index = increment_opt(False, self.code_options, self.code_index)
        self.update_display()
        self.warm_down = 4