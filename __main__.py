#from  music.album import Album
from music.artist import Artist
from credentials import SpotifyManager
from threading import Thread

def GetArtist():

    name = input("Enter an artists name:\n") # chosen artist
    spotify_manager = SpotifyManager()
    sp = spotify_manager.GetCertified()
    result = sp.search(name)
    #pull all of the artists albums
    artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
    sp_albums = sp.artist_albums(artist_uri,album_type='album')
    artist = Artist(name, sp_albums)
    artist.GetAlbumNames()
    return artist

t1 = Thread(target=GetArtist, args=())
t1.start()
t1.join()



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
