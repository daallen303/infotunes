from graph import Graph
from music.album import Album
from music.song import Song
from music.artist import Artist
from credentials import SpotifyManager 
import threading
import queue
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
    track = sp.track(track_uri)
    audio_analysis = sp.audio_analysis(track_uri)
    audio_features = sp.audio_features(track_uri)
    song = Song(track, audio_features, audio_analysis)
    return song

def GetAlbum(in_album):
    
    tracks = sp.album_tracks(in_album['uri'])
    sp_album = sp.album(in_album['uri'])
    songs = [] 

    #for i in range(len(tracks['items'])):
    #    songs.append(GetSong(tracks['items'][i]['uri']))
    #songs = []
    #threads = []
    album = Album(sp_album, songs, len(tracks['items']))
    return album

def GetArtist(artist):
    sp_albums = sp.artist_albums(artist['uri'], limit=10)
    albums = []
    album_names = []
    for i in range(len(sp_albums['items'])):
        if sp_albums['items'][i]['type'] == 'album' and sp_albums['items'][i]['name'] not in album_names:
            albums.append(GetAlbum(sp_albums['items'][i]))
            album_names.append(sp_albums['items'][i]['name'])
    return Artist(artist, albums) 

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
start = time.time()
GetPlaylist()
end = time.time()
print("Program took "+str(end-start)+" seconds")
#name = input("Enter a band name:\n")
#result = sp.search(name, limit=1, type='artist')
#artist = GetArtist(result['artists']['items'][0])
#Graph.AlbumPopularityOverTime(artist)
