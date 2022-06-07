import pykka, time
import logging
from mopidy import core

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO

# Pin Config
RST = None

SWITCH_PIN = 17
ENC_DT_PIN = 9
ENC_CLK_PIN = 10

from .display import draw_data

logger = logging.getLogger(__name__)

class PiRotaryEncoder:
    
    def __init__(self, dt_pin, clk_pin, bouncetime=5):
        self.dt_pin, self.clk_pin = dt_pin, clk_pin
        GPIO.setup(self.dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.clk_pin, GPIO.RISING, 
            callback=self.clock_tick, bouncetime=bouncetime)
        self.clk_last_state = GPIO.input(self.clk_pin)
        self.callback = None
    
    def clock_tick(self, channel):
        clk_state = GPIO.input(self.clk_pin)
        dt_state = GPIO.input(self.dt_pin)
        if clk_state != self.clk_last_state:
            direc = dt_state != clk_state
            if self.callback: self.callback(direc)
    
    def register_callback(self, callback):
        self.callback = callback

class RadioooooFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(RadioooooFrontend, self).__init__()
        self.core = core
        # Display Setup
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
        self.disp.begin()
        self.disp.clear()
        self.disp.display()
        # Frontend State
        self.display_options = ["Country", "Year"]
        self.display_index = 0
        self.warm_down = 4
        # Options
        self.year_options = [ str(1900 + (i*10)) for i in range(0,12)]
        self.code_options = [ "LKA", "AGO", "RUS", "CHN", "JPN", "THA"]
        self.year_index = 8
        self.code_index = 0
        # Setup Buttons
        GPIO.setmode(GPIO.BCM)
        # Setup Switch & Encoder
        GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(SWITCH_PIN, GPIO.RISING, bouncetime=100, callback=self.switch_mode)
        encoder = PiRotaryEncoder(ENC_DT_PIN, ENC_CLK_PIN)
        encoder.register_callback(self.update_options)

    def on_start(self):
        self.update_display()
        while True:
            self.warm_down = self.warm_down - 1
            if self.warm_down == 0:
                channel = f"radiooooo:{self.year_options[self.year_index]}:{self.code_options[self.code_index]}"
                logger.debug(f"Playing Now {channel}")
                self.core.playback.stop()
                self.core.tracklist.clear()
                self.core.tracklist.add(uris=[channel])
                self.core.playback.play()
            elif self.warm_down == -10:
                self.disp.clear()
                self.disp.display()
            elif self.warm_down < -10:
                self.warm_down = -11
            time.sleep(1)

    def on_stop(self):
        self.disp.clear()
        self.disp.display()

    def update_display(self):
        draw_data(self.disp, {
            "code": self.code_options[self.code_index],
            "year": self.year_options[self.year_index]
        })
    
    def switch_mode(self, channel):
        self.display_index = self.handle_options(True, self.display_options, self.display_index)
        self.warm_down = 4
        logger.debug(f"Current Mode Is {self.display_options[self.display_index]}")
    
    def update_options(self, direc):
        if self.display_index == 0:
            self.code_index = self.handle_options(direc, self.code_options, self.code_index)
        elif self.display_index == 1:
            self.year_index = self.handle_options(direc, self.year_options, self.year_index)
        self.warm_down = 4
        self.update_display()

    def handle_options(self, increment, options, idx):
        n_idx = idx + 1 if increment else idx - 1
        if n_idx < 0:
            n_idx = len(options) -1
        elif n_idx >= len(options):
            n_idx = 0
        return n_idx