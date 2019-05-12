import spotipy
from spotipy.oauth2 import SpotifyClientCredentials  
from enum import Enum

class Key(Enum):
    
    C = 0
    Db = 1
    D = 2
    Eb = 3
    E = 4
    F = 5
    Gb = 6
    G = 7
    Ab = 8
    A = 9
    Bb = 10
    B = 11

# Converts intergers into keys 


class Song:

    def __init__(self, track):
        self.id = track['id']
        self.name = track['name']
        
        audio_features = sp.audio_features(track['id'])
        self.acousticness = audio_features[0]['acousticness']
        self.key = audio_features[0]['key']
        self.danceability= audio_features[0]['danceability']

    def GetName(self):
        return self.name

    def GetKey(self):
        return Key(self.key).name
        

#Class for storing all information about a song

class Album:

    def __init__(self, name, uri):
        
        self.uri = uri
        self.name = name
        self.songs = []        

        #create keys-values of empty lists inside nested dictionary for album
        

        tracks = sp.album_tracks(self.uri) 
        
        for n in range(len(tracks['items'])): #for each song track
            self.songs.append(Song(tracks['items'][n])) 

    def PrintAlbumInfo(self):
        for song in self.songs:
            print(song.GetName(), song.GetKey())

# Class for storing all information about an album

class Artist:
    
    def __init__(self,name):
        self.name = name
        result = sp.search(name)

        # extract artist uri
        self.uri = result['tracks']['items'][0]['artists'][0]['uri']

        #pull all of the artists albums
        sp_albums = sp.artist_albums(self.uri,album_type='album')

        #store artists album uris in seperate lists
        self.album_uris = []
        self.album_names = []
        for i in range(len(sp_albums['items'])):
            if self.album_uris == [] or sp_albums['items'][i]['name'] not in self.album_names:
                self.album_uris.append(sp_albums['items'][i]['uri'])
                self.album_names.append(sp_albums['items'][i]['name'])

# Class for artist information



def GetCertified(client_id, client_secret):
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)

    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


client_id = "e2e1e1eca1bf4883a109f3d4a30b3400"
client_secret = "ba975017397d4b13aad38f876b5b99ad"
sp = GetCertified(client_id, client_secret);


name = input("Enter an artists name:\n") # chosen artist
artist = Artist(name)

#key = input("What would you like to know?")

albums = []
count = 0

print("Songs and albums from", artist.name)
for name in artist.album_names:
    albums.append(Album(name, artist.album_uris[count]))
    print("Album: ",name)
    albums[count].PrintAlbumInfo()
    count+=1

