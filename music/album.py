from .song import Song
from .musiccred import SpotifyManager 

class Album:

    def __init__(self, uri, name):
        
        self.uri = uri
        self.name = name
        self.songs = []

        #create keys-values of empty lists inside nested dictionary for album
        spotify_manager = SpotifyManager()
        sp = spotify_manager.GetCertified()
        tracks = sp.album_tracks(self.uri) 
        
        for n in range(len(tracks['items'])): #for each song track
            self.songs.append(Song(tracks['items'][n], sp)) 

    def PrintAlbumInfo(self):
        for song in self.songs:
            print(song.GetName(), song.GetKey())
    def GetName(self):
        return self.name
# Class for storing all information about an album

