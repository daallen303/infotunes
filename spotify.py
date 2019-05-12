import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 

class Album:


    def __init__(self, name,uri):
        
        self.uri = uri
        self.name = name
        
        self.info = {} #creates dictionary for that specific album

        #create keys-values of empty lists inside nested dictionary for album
        self.info['track_number'] = []
        self.info['song_id'] = []
        self.info['song_name'] = []
        self.info['song_uri'] = []

        tracks = sp.album_tracks(self.uri) 
 
        for n in range(len(tracks['items'])): #for each song track
            self.info['track_number'].append(tracks['items'][n]['track_number'])
            self.info['song_id'].append(tracks['items'][n]['id'])
            self.info['song_name'].append(tracks['items'][n]['name'])
            self.info['song_uri'].append(tracks['items'][n]['uri'])

    def PrintInfo(self, key):
        for i in self.info[key]:
            print(i)
        


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
            self.album_uris.append(sp_albums['items'][i]['uri'])
            self.album_names.append(sp_albums['items'][i]['uri'])

# Class for artist information



def GetCertified(client_id, client_secret):
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)

    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


client_id = "e2e1e1eca1bf4883a109f3d4a30b3400"
client_secret = "ba975017397d4b13aad38f876b5b99ad"
sp = GetCertified(client_id, client_secret);


name = input("Enter an artists name:\n") # chosen artist
artist = Artist(name)

albums = []
count = 0

print("Songs and albums from", artist.name)
for name in artist.album_names:
    albums.append(Album(name, artist.album_uris[count]))
    print(name)
    albums[count].PrintInfo('song_name')
    count+=1

