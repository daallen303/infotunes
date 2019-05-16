#from  music.album import Album
#from music.artist import Artist
#from music.album import Album
from music.song import Song
from credentials import SpotifyManager
from threading import Thread

spotify_manager = SpotifyManager()
sp = spotify_manager.GetCertified()

def GetArtistsAlbums(sp_albums):
    albums = []
    album_names = []
    album_uris = []
    songs = []

    count = 0
    
    for i in range(len(sp_albums['items'])):
        if albums == [] or sp_albums['items'][i]['name'] not in album_names:
            album_names.append(sp_albums['items'][i]['name'])
            album_uris.append(sp_albums['items'][i]['uri'])
            albums.append(Album(sp_albums['items'][i]['uri'], sp_albums['items'][i]['name']))
            tracks = sp.album_tracks(sp_albums['items'][i]['uri'])
            for i in range(len(tracks['items'])):
                audio_features = sp.audio_features(tracks['items'][i]['uri'])
                songs.append(Song(tracks['items'][i]['name'], tracks['items'][i]['uri'], audio_features))
                albums[count].AddSong(songs[count])
            count+=1

    return (albums, songs, album_names, album_uris)
    
def GetSongsFromAlbum(tracks):

    audio_features = sp.audio_features(track['id'])

#t1 = Thread(target=GetArtist, args=())
#t1.start()
#t1.join()

name = "six60" 
result = sp.search(name)

artist_uri = result['tracks']['items'][0]['artists'][0]['uri']

artist = Artist(name, artist_uri)
sp_albums = sp.artist_albums(artist_uri ,album_type='album')
# (albums, songs, album_names, album_uris)
tuple = GetArtistsAlbums(sp_albums)
artist.SetAlbums(tuple[2], tuple[3])
albums = tuple[0]
songs = tuple[1]
print(albums[0].GetName())
print(albums[0].GetSongNames())
print(songs[0].GetKey())
"""
albums = []
count = 0

print("Songs and albums from", artist.name)
for name in artist.album_names:
    albums.append(Album(name, artist.album_uris[count]))
    print("Album: ",name)
    albums[count].PrintAlbumInfo()
    count+=1
user_name = User("daallen-us")
sp.search(user_name)

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

scope = 'playlist-read-collaborative'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
auth = SpotifyOAuth(client_id, client_secret, redirect_uri )

if token:
    sp.trace = False
    ranges = ['short_term','meduim_term', 'long_term']
    for range in ranges:
        print("range:", range)
        results = sp.current_user_playlists()
        #for i, item in enumerate(results['item']):
         #   print(i, item['name'])
          #  print()
else:
    print("Can't get token for", username)

top_artists = sp.current_user_top_artists(limit=10,offset=0, time_range='medium_term')"""
