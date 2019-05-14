from .audioinfo import Key

class Song:

    def __init__(self, name, uri, audio_features):
        self.uri = uri
        self.name = name
        
        self.acousticness = audio_features[0]['acousticness']
        self.key = audio_features[0]['key']
        self.danceability= audio_features[0]['danceability']

    def GetName(self):
        return self.name

    def GetKey(self):
        return Key(self.key).name
    def GetDanceability(self):
        return self.danceability
        

#Class for storing all information about a song

