import pykka, time
from mopidy import core

class RadioooooFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(RadioooooFrontend, self).__init__()
        self.core = core