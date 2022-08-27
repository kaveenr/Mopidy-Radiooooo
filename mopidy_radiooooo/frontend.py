import pykka, time
import logging
from mopidy import core
import os

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO

SWITCH_PIN = 17
ENC_DT_PIN = 22
ENC_CLK_PIN = 27

VOL_DT_PIN = 5
VOL_CLK_PIN = 6

SDOWN_PIN = 20

from .display import OLEDDisplay
from .io import PiRotaryEncoder

logger = logging.getLogger(__name__)

class RadioooooFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(RadioooooFrontend, self).__init__()
        self.core = core
        # Display Setup
        self.disp = OLEDDisplay('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
        self.disp.clear()
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
        vol_encoder = PiRotaryEncoder(VOL_DT_PIN, VOL_CLK_PIN)
        vol_encoder.register_callback(self.set_volume)
        # Setup Shutdown Button
        GPIO.setup(SDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(SDOWN_PIN, GPIO.RISING, callback=self.shutdown)

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
            elif self.warm_down < -10:
                self.warm_down = -11
            time.sleep(1)

    def on_stop(self):
        self.disp.clear()

    def update_display(self):
        if self.display_index == 0:
            self.disp.draw_country(self.code_options[self.code_index])
        elif self.display_index == 1:
            self.disp.draw_year(self.year_options[self.year_index])
    
    def switch_mode(self, channel):
        self.display_index = self.handle_options(True, self.display_options, self.display_index)
        self.warm_down = 4
        logger.debug(f"Current Mode Is {self.display_options[self.display_index]}")
    
    def update_options(self, direc):
        logger.debug(f"Select Encoder Tick {direc}")
        if self.display_index == 0:
            self.code_index = self.handle_options(direc, self.code_options, self.code_index)
        elif self.display_index == 1:
            self.year_index = self.handle_options(direc, self.year_options, self.year_index)
        self.warm_down = 4
        self.update_display()

    def set_volume(self, direc):
        cur_vol = self.core.mixer.get_volume().get()
        self.core.mixer.set_volume(cur_vol + 5 if direc else  cur_vol - 5)
        logger.debug(f"Volume Encoder Tick {direc}")

    def handle_options(self, increment, options, idx):
        n_idx = idx + 1 if increment else idx - 1
        if n_idx < 0:
            n_idx = len(options) -1
        elif n_idx >= len(options):
            n_idx = 0
        return n_idx
    
    def shutdown(self, channel):
        logger.info("Shutting down system!")
        os.system("sudo shutdown -h now")