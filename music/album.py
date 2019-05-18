from .song import Song

class Album:

    def __init__(self, album, songs, song_count):
       
        self.uri = album['uri']
        self.name = album['name']
        self.songs = songs
        self.album_type = album['album_type']
        self.artist = album['artists'][0]['name']
        self.release_date = album['release_date']
        self.release_date_precision = album['release_date_precision']
        self.genres = album['genres']
        self.images = album['images']
        self.popularity = album['popularity']
        self.song_count = song_count

        

    def GetSongNames(self):
        return self.song_names

    def GetName(self):
        return self.name

# Class for storing all information about an album

