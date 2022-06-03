import pykka
import requests
import json

from mopidy import backend, models
from .constants import lookup_code

BASE_URL = "https://radiooooo.com"

def get_track(year, country):
    headersList = {
        "Content-Type": "application/json" 
    }

    payload = {
        "mode": "explore",
        "isocodes": [country],
        "decades": [year],
        "moods": ["SLOW","FAST"]
    }

    response = requests.request(
        "POST", 
        f"{BASE_URL}/play",
        data=json.dumps(payload),
        headers=headersList
    )
    return response.json()

def get_countries(year):
    response = requests.request(
        "GET",
        f"{BASE_URL}/country/mood?decade={year}"
    )
    return response.json()

class RadioooooPlaybackProvider(backend.PlaybackProvider):

    def __init__(self, audio, backend):
        super(RadioooooPlaybackProvider, self).__init__(audio, backend)
        self.track = None
        self.uri = None

    def advance_track(self):
        parts = self.uri.split(":")
        year, country = int(parts[1]), parts[2]
        self.track = get_track(int(parts[1]), parts[2])
        meta = models.Track(
            uri= self.uri,
            name=self.track["title"],
            artists=[models.Artist(uri="unk", name=self.track["artist"])],
            length=self.track["length"] * 1000
        )
        self.audio.set_metadata(meta)

    def current_track_url(self):
        return self.track["links"][list(self.track["links"].keys())[0]]

    def change_track(self, track):
        self.uri = track.uri
        self.advance_track()
        return True

    def play(self):
        self.audio.prepare_change()
        self.audio.set_uri(self.current_track_url())
        self.audio.start_playback()
        self.audio.set_about_to_finish_callback(self.about_to_end).get()
        return True

    def about_to_end(self):
        self.advance_track()
        self.audio.set_uri(self.current_track_url()).get()


class RadioooooLibraryProvider(backend.LibraryProvider):
    
    root_directory = models.Ref.directory(uri='radiooooo:', name='Radiooooo')

    def browse(self, uri):
        if uri == self.root_directory.uri:
            yearfolder = lambda year: models.Ref.directory(
                uri=f"radiooooo:{year}",
                name=f"{year}"
            )
            return [
                yearfolder(1900 + (i*10))
                for i in range(0,12)
            ]
        
        parts=uri.split(":")        
        if len(parts) == 2:
            options = get_countries(parts[1])
            country_set = set()
            for mood in options.keys():
                for country in options[mood]:
                    country_set.add(country)
            return [ 
                models.Ref.track(
                    uri=f"radiooooo:{parts[1]}:{country}",
                    name=f"{lookup_code(country)}"
                ) 
                for country in country_set
            ]
        
        return []

    def lookup(self, uri=None, uris=None):
        if uri:
            parts = uri.split(':')
            if len(parts) == 3:
                track = models.Track(
                    uri= uri,
                    name=f"{lookup_code(parts[2])} ({parts[1]})"
                )
                return [ track ]
            return None
        else:
            return {uri: self.lookup(uri=uri) for uri in uris}

class RadioooooBackend(pykka.ThreadingActor, backend.Backend):
    uri_schemes = ['radiooooo']
    
    def __init__(self, config, audio):
        super(RadioooooBackend, self).__init__()
        self.library = RadioooooLibraryProvider(backend=self)
        self.playback = RadioooooPlaybackProvider(audio=audio, backend=self)