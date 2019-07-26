from .song import Song
import datetime

class Album:

    def __init__(self, album, songs, song_count):
       
        self.uri = album['uri']
        self.name = album['name']
        self.songs = songs
        self.album_type = album['album_type']
        self.artist = album['artists'][0]['name']
        self.release_date_precision = album['release_date_precision']
        if self.release_date_precision == "day":
            day = album['release_date'][8:]
            month = album['release_date'][5:7]
            year = album['release_date'][:4]
            self.release_date = datetime.datetime.strptime(month+"-"+day+"-"+year, "%m-%d-%Y")
        elif self.release_date_precision == "month":
            month = album['release_date'][6:7]
            year = album['release_date'][:4]
            self.release_date = datetime.datetime.strptime(month+"-01-"+year, "%m-%d-%Y")
        else:
            self.release_date = datetime.datetime.strptime("01-01-"+album['release_date'], "%m-%d-%Y")
        self.genres = album['genres']
        self.images = album['images']
        self.popularity = album['popularity']
        self.song_count = song_count

        

    def GetSongNames(self):
        return self.song_names

    def GetName(self):
        return self.name

# Class for storing all information about an album

