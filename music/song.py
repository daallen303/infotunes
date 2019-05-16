from .audioinfo import Key
#from .audioinfo import mode

class Song:

    def __init__(self, track, audio_features, audio_analysis):
        self.uri = track['uri']
        self.name = track['name']
        #self.popularity = track['popularity']
        self.track_number = track['track_number']
        self.preview_url = track['preview_url']
        #self.disk_number = track['disk_number']
        #self.album_name = track['album']['name']
        
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


    def GetName(self):
        return self.name

    def GetKey(self):
        return Key(self.key).name
    def GetDanceability(self):
        return self.danceability
        

#Class for storing all information about a song

