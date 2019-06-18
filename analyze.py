from graph import Graph
from music.album import Album
from music.song import Song
from music.artist import Artist
from credentials import SpotifyManager 
import spotipy.util as util
import spotipy
import sys
import time 

spotify_manager = SpotifyManager()
sp = spotify_manager.GetCertified()

def ConvertSearch(name):
    for i in range(len(name)):
        if name[i] == ' ':
           name[i] == '+'
    return name

def GetSong(track_uri):   
    name = input("Enter the song's name \n")
    # Also have a thing to enter the artists name
    result = sp.search(q='song:'+name, type='track') 
    track = sp.track(result['track']['items'][0])
    audio_analysis = sp.audio_analysis(track_uri)
    audio_features = sp.audio_features(track_uri)
    song = Song(track, audio_features, audio_analysis)
    return song

def GraphSong():
    print("graph song function calls")

def GetAlbum(album=None):
    if album == None:
        name = input("Enter the album's name\n")
        result = sp.search(q='album:'+ name, type='album')
        album = result['albums']['items'][0] 
    tracks = sp.album_tracks(album['uri'])
    sp_album = sp.album(album['uri'])
    songs = [] 
    album = Album(sp_album, songs, len(tracks['items']))
    return album

def GraphAlbum():
    print("graph song function calls")

def GetArtist():
    name = input("Enter the artist's name\n")
    result = sp.search(q='artist:' + name, type='artist')
    print(result)
    artist = result['artists']['items'][0]
    print(artist)
    sp_albums = sp.artist_albums(artist['uri'], limit=50)
    albums = []
    album_names = []
    for i in range(len(sp_albums['items'])):
        if sp_albums['items'][i]['type'] == 'album' and sp_albums['items'][i]['name'] not in album_names:
            albums.append(GetAlbum(sp_albums['items'][i]))
            album_names.append(sp_albums['items'][i]['name'])
    return Artist(artist, albums) 

def GraphArtist():
    print("graph artist") 
    
    
def GetAllSongsFromArtist(artist):
    songs = []
    for i in len(artist.albums):
        for song in albums[i]:
            songs.append(song)
    return songs

def GetAverage(songs, name):
    danceability = speechiness = energy = acousticness = instrumentalness = liveness = count = 0
    for song in songs:
        danceability += song.danceability
        speechiness += song.speechiness
        energy += song.energy
        acousticness += song.acousticness
        instrumentalness += song.instrumentalness
        liveness += song.liveness
        count += 1
    danceability = danceability/count
    speechinees = speechiness/count
    energy = energy/count
    acousticness = acousticness/count
    instrumentalness = instrumentalness/count
    liveness = liveness/count
    average_song = Song()
    average_song.SetFeatures("Average "+ name, danceability, speechiness, energy, acousticness, instrumentalness, liveness)
    return average_song

def GetPlaylist():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username " % (sys.argv[0],))
        sys.exit()

    scope = 'playlist-modify-public user-read-email'
    token = util.prompt_for_user_token(username, scope)

    if token:
        spot = spotipy.Spotify(auth=token)
        spot.trace = False
        playlist = spot.user_playlists(username)
        songs = []
        for i in range(0,4):
            tracks = sp.user_playlist_tracks(username, playlist_id='spotify:playlist:3scjzNJ1Akyzsc4rPwGZtT', limit = 1, offset=i)
            print(range(len(tracks['items'])))
            for i in range(len(tracks['items'])):
                songs.append(GetSong(tracks['items'][i]['track']['uri']))
        Graph.GraphPlaylist(songs, playlist['items'][1]['name'])
    else:
        print("Can't get token for", username)

def GraphPlaylist():
    print("graph playlist")

print("\n\nWelcome to InfoTunes \nWhat would you like information about? \n") 
option = input("Type 'a' for artist, 's' for song, 'al' for album, 'p' for playlist, 'q' to quit and exit \n")


while option != 'q':
    if option == 'a':
        GetArtist()
    elif option == 's':
        GetSong()
    elif option == 'al':
        GetAlbum()
    elif option == 'p':
        GetPLaylist()
    else:
        print("Value not understood, please enter a valid value")
        
    option = input("Type 'a' for artist, 's' for song, 'al' for album, 'p' for playlist, 'q' to quit and exit \n")






