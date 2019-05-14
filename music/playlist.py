class Playlist:

    def __init__(self, playlist):
        self.name = playlist['name']
        self.owner = playlist['owner']
        self.tracks = playlist['tracks']
        
        print(self.name)
# Class for storing information about a specific playlist

