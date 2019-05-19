from graph import Graph
from music.album import Album
from music.song import Song
from music.artist import Artist
from credentials import SpotifyManager 
import threading
import queue

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
    sp_albums = sp.artist_albums(artist['uri'], limit=50)
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

#Graph.AlbumPopularityOverTime()
name = input("Enter a band name:\n")
result = sp.search(name, limit=1, type='artist')
artist = GetArtist(result['artists']['items'][0])
Graph.AlbumPopularityOverTime(artist)


#Graph.RadarPlot(song)
#song = GetSong(result['tracks']['items'][0])
#Graph.GraphSongFeatures(song)
#print(result['artists']['items'][0]['name'])
#average = GetAllSongsFromArtist(artist)
#GraphSongFeatures(average)
#sp_album = result['albums']['items'][0]
#album = GetAlbum(sp_album)
#GraphKey(album.songs)
#average = GetAverage(album.songs, album.name)
#GraphSongFeatures(average)
#for song in album.songs:
#    print(song.name)
    
    
"""print(len(tracks['items']))
for i in range(len(tracks['items'])):
    track = tracks['items'][i]
    t = threading.Thread(target=lambda q, arg1: q.put(GetSong(track)), args=(que,track,))
    threads.append(t)
    t.start()
    songs.append(GetSong(track))
for t in threads:
    t.join()
    songs.append(que.get())"""
