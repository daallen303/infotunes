from .audioinfo import Key

class Song:

    def __init__(self, track, sp):
        self.id = track['id']
        self.name = track['name']
        self.sp = sp
        
        audio_features = sp.audio_features(track['id'])
        self.acousticness = audio_features[0]['acousticness']
        self.key = audio_features[0]['key']
        self.danceability= audio_features[0]['danceability']

    def GetName(self):
        return self.name

    def GetKey(self):
        return Key(self.key).name
        

#Class for storing all information about a song

