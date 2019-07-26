from .album import Album

class Artist:
    
    def __init__(self, artist, albums, top_tracks_name, top_tracks_popularity):
        self.name = artist['name']
        self.uri = artist['uri']
        self.albums = albums
        self.genres = artist['genres']
        self.top_tracks_name = top_tracks_name
        self.top_tracks_popularity = top_tracks_popularity
        #self.similar_artist = artist['similar_artist']
        self.popularity = artist['popularity']
        self.first_release = albums[0].release_date
        self.last_release = albums[-1].release_date
    
    def SetAlbums(self, album_names, album_uris):
        #store artists albums and album_names in seperate lists
        self.album_uris = album_uris
        self.album_names = album_names


    def GetAlbumNames(self):
        return album_names
    
    def GetUri(self):
        return self.uri    

# Class for artist information

