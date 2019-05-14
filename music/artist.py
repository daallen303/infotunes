from .album import Album

class Artist:
    
    def __init__(self, name, uri):
        self.name = name
        self.uri = uri
        #genres
        #similar artist
        #popularity
        #First album release date
        #Last album release date
    
    def SetAlbums(self, album_names, album_uris):
        #store artists albums and album_names in seperate lists
        self.album_uris = album_uris
        self.album_names = album_names


    def GetAlbumNames(self):
        return album_names
    def GetUri(self):
        return self.uri

# Class for artist information

