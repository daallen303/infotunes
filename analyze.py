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

def GetSong(track_uri=None):   
    if track_uri == None:
        song_name = input("Enter the song's name \n")
        artist_name = input("Enter the artist's name \n")
        # Also have a thing to enter the artists name
        query =  "artist:%"+artist_name+" track:%"+song_name
        result = sp.search(q=query, type='track')
        print("Getting Information about "+song_name)
        track = sp.track(result['tracks']['items'][0]['uri'])
    else:
        track = sp.track(track_uri)
    audio_analysis = sp.audio_analysis(track['uri'])
    audio_features = sp.audio_features(track['uri'])
    song = Song(track, audio_features, audio_analysis)
    return song

def GraphSong(song):
    Graph.AudioFeaturesRadarPlot(song)
    Graph.AudioFeaturesBarGraph(song)
    # audio features bar graph and spider graph thingy etc.

def GetAlbum(album=None, full_info=False):
    if album == None:
        album_name = input("Enter the album's name\n")
        artist_name = input("Enter the artist's name\n")
        query = "artist:%"+artist_name+" album:%"+album_name
        result = sp.search(q=query, type='album')
        album = result['albums']['items'][0] 
    tracks = sp.album_tracks(album['uri'])
    sp_album = sp.album(album['uri'])
    songs = []
    if full_info == True:
        print("Getting Information about the songs in "+album_name)
        for i in range(2):
            songs.append(GetSong(tracks['items'][i]['uri']))
            print(songs[i].name)
    album = Album(sp_album, songs, len(tracks['items']))
    return album

def GraphAlbum(album):
    average_song = GetAverageSong(album.songs, album.name)
    Graph.AlbumKeys(album.songs)
    Graph.AudioFeaturesRadarPlot(average_song)
    Graph.AudioFeaturesBarGraph(average_song)

def GetArtist():
    name = input("Enter the artist's name\n")
    print("Generating information about " + name)
    result = sp.search(q='artist:' + name, type='artist')
    artist = result['artists']['items'][0]
    print(artist)
    sp_albums = sp.artist_albums(artist['uri'], limit=3)
    albums = []
    album_names = []
    print("\n Collecting album names:\n")
    for i in range(len(sp_albums['items'])):
        if sp_albums['items'][i]['type'] == 'album' and sp_albums['items'][i]['name'] not in album_names:
            print(sp_albums['items'][i]['name'])
            albums.append(GetAlbum(sp_albums['items'][i]))
            album_names.append(sp_albums['items'][i]['name'])
    return Artist(artist, albums) 

def GraphArtist(artist):
    Graph.AlbumPopularityOverTime(artist)
    
    
def GetAllSongsFromArtist(artist):
    songs = []
    for i in len(artist.albums):
        for song in albums[i]:
            songs.append(song)
    return songs

def GetAverageSong(songs, name):
    tempo = popularity = valence = loudness = duration_ms = danceability = speechiness = energy = acousticness = instrumentalness = liveness = count = 0
    for song in songs:
        danceability += song.danceability
        speechiness += song.speechiness
        energy += song.energy
        acousticness += song.acousticness
        instrumentalness += song.instrumentalness
        liveness += song.liveness
        tempo += song.tempo
        popularity += song.popularity
        valence += song.valence
        loudness += song.loudness
        duration_ms += song.duration_ms
        count += 1
    danceability = danceability/count
    speechinees = speechiness/count
    energy = energy/count
    acousticness = acousticness/count
    instrumentalness = instrumentalness/count
    liveness = liveness/count
    tempo = tempo/count
    popularity = popularity/count
    valence = valence/count
    loudness = loudness/count
    duration_ms = duration_ms/count
    average_song = Song()
    average_song.SetFeatures("Average "+ name, danceability, speechiness, energy, acousticness, instrumentalness, liveness, tempo, popularity, valence, loudness, duration_ms)
    return average_song

def GetUser():
    username = input("Please enter your username\n")
    scope = 'playlist-modify-public user-read-email'
    token = util.prompt_for_user_token(username, scope)

    if token:
        spot = spotipy.Spotify(auth=token)
        spot.trace = False
       # playlist = spot.user_playlists(username)
       # songs = []
       # for i in range(0,4):
       #     tracks = sp.user_playlist_tracks(username, playlist_id='spotify:playlist:3scjzNJ1Akyzsc4rPwGZtT', limit = 1, offset=i)
       #     print(range(len(tracks['items'])))
       #     for i in range(len(tracks['items'])):
       #         songs.append(GetSong(tracks['items'][i]['track']['uri']))
    else:
        print("Can't get token for", username)

def GetPlaylist():
    name = input("Please input the playlists name\n")
    result = sp.search(q='playlist:' + name, type='playlist')
    print(result['playlists']['items'][0]['uri'])

def GraphPlaylist(songs):
    Graph.GraphPlaylist(songs)

print("\n\nWelcome to InfoTunes \nWhat would you like information about? \n") 
option = input("Type 'a' for artist, 's' for song, 'al' for album, 'p' for playlist, 'q' to quit and exit \n")


while option != 'q':
    if option == 'a':
        artist = GetArtist()
        GraphArtist(artist)
    elif option == 's':
        song = GetSong()
        GraphSong(song)
    elif option == 'al':
        album = GetAlbum(full_info=True)
        GraphAlbum(album)
    elif option == 'p':
        playlist = GetPlaylist()
        GraphPlaylist(playlist.songs)
    elif option == 'u':
        user = GetUser()
        GraphUser(user)
    else:
        print("Value not understood, please enter a valid value") 
    option = input("Type 'a' for artist, 's' for song, 'al' for album, 'p' for playlist, 'q' to quit and exit \n")






