import RPi.GPIO as GPIO

class PiRotaryEncoder:
    
    callback = None
    def __init__(self, dt_pin, clk_pin, bouncetime=1):
        self.dt_pin, self.clk_pin = dt_pin, clk_pin
        GPIO.setup(self.dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        self.clk_state, self.dt_state = GPIO.input(self.dt_pin), GPIO.input(self.clk_pin)
        GPIO.add_event_detect(self.clk_pin, GPIO.BOTH, 
            callback=self.__encoder_event, bouncetime=bouncetime)
        GPIO.add_event_detect(self.dt_pin, GPIO.BOTH, 
            callback=self.__encoder_event, bouncetime=bouncetime)
    
    def __encoder_event(self, channel):
        cur_clk_state, cur_dt_state  = GPIO.input(self.dt_pin), GPIO.input(self.clk_pin)
        if self.clk_state != cur_clk_state:
            change = cur_dt_state != self.clk_state
            if self.callback : self.callback(not change)
        self.clk_state, self.dt_state = cur_clk_state, cur_dt_state 

    def register_callback(self, callback):
        self.callback = callback