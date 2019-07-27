from .audioinfo import Key
#from .audioinfo import mode

class Song:

    def __init__(self, track=None, audio_features=None, audio_analysis=None):
        if track is not None:
            self.uri = track['uri']
            self.name = track['name']
            self.popularity = track['popularity']
            self.track_number = track['track_number']
            self.preview_url = track['preview_url']
            self.release_date = track['album']['release_date']
            #self.disk_number = track['disk_number']
            self.artist = track['artists'][0]['name']
            self.album_name = track['album']['name']
            self.track_number = track['track_number']
            
            # audio features 
            af = audio_features[0]
            self.duration_ms = af['duration_ms'] 
            self.key = af['key'] # 0-11 C=0 Db=1 D=2 ...etc
            self.mode = af['mode'] # major = 1 minor = 0
            self.time_sig = af['time_signature'] # beats per measure 
            self.loudness = af['loudness'] # in decibels
            self.tempo = af['tempo'] #bpm
            self.valence = af['valence'] # high valence means it sounds possitive low = negative

            self.danceability= af['danceability'] # 0-1
            self.speechiness = af['speechiness'] # 0-1
            self.energy = af['energy'] # 0-1
            self.acousticness = af['acousticness'] # 0-1
            self.instrumentalness = af['instrumentalness'] # 0-1
            self.liveness = af['liveness'] # 0-1
            # audio_analysis
            """Could be added to potentially grab the chord changes in a song
            and a lot of other more in depth knowledge not needed currently"""

    #constructor for song that takes in average values of a group of songs
    def SetFeatures(self, name, danceability, speechiness, energy, acousticness, instrumentalness, liveness, tempo, popularity, valence, loudness, duration_ms):
        self.name = name
        self.danceability= danceability # 0-1
        self.speechiness = speechiness # 0-1
        self.energy = energy # 0-1
        self.acousticness = acousticness # 0-1
        self.instrumentalness = instrumentalness # 0-1
        self.liveness = liveness # 0-1
        self.tempo = tempo # in bpm
        self.popularity = popularity # 0-100
        self.valence = valence 
        self.loudness = loudness # in db
        self.duration_ms = duration_ms # in ms

    def GetName(self):
        return self.name

    def GetKey(self):
        return Key(self.key).name
    def GetDanceability(self):
        return self.danceability
        

#Class for storing all information about a song

