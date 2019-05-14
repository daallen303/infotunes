from .album import Album

class Artist:
    
    def __init__(self, name, sp_albums):
        self.name = name
        self.sp_albums = sp_albums

        #store artists albums and album_names in seperate lists
        self.albums = []
        self.album_names = []

        for i in range(len(sp_albums['items'])):
            if self.albums == [] or sp_albums['items'][i]['name'] not in self.album_names:
                self.albums.append(Album(sp_albums['items'][i]['uri'], sp_albums['items'][i]['name']))
                self.album_names.append(sp_albums['items'][i]['name'])
                print(len(self.albums))

    def GetAlbumNames(self):
        for album in self.albums:
            print(album.GetName())
            print(album.PrintAlbumInfo())

# Class for artist information

