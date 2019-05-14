from .song import Song

class Album:

    def __init__(self, uri, name):
        
        self.uri = uri
        self.name = name
        self.song_names = []
        self.song_uris = []
        
    def SetSongs(self, song_names, song_uris):
        self.song_names = song_names
        self.song_uris = song_uris

    def GetSongNames(self):
        return self.song_names

    def GetName(self):
        return self.name

# Class for storing all information about an album

