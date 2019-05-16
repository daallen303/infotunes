from music.album import Album
from music.song import Song
from music.artist import Artist
from credentials import SpotifyManager 
import matplotlib.pyplot as plt 
import numpy as np
import threading
import queue

spotify_manager = SpotifyManager()
sp = spotify_manager.GetCertified()

def GraphSongFeatures(song):
    
    labels = ('danceability', 'speechiness', 'acousticness','energy', 'instrumentalness', 'liveness')
    y_pos = np.arange(len(labels))
    confidence = [song.danceability, song.speechiness, song.acousticness, song.energy, song.instrumentalness, song.liveness]

    plt.bar(y_pos, confidence, align='center', alpha=.1, color='blue',linewidth=1)
    plt.xticks(y_pos, labels)
    plt.ylabel('Confidence')
    plt.title(song.name +' Song Features')
    plt.ylim(0,1)
    plt.show()

def ConvertSearch(name):
    for i in range(len(name)):
        if name[i] == ' ':
           name[i] == '+'
    return name

def GetSong(track):   
    track_uri = track['uri']
    audio_analysis = sp.audio_analysis(track_uri)
    audio_features = sp.audio_features(track_uri)
    song = Song(track, audio_features, audio_analysis)
    return song

def GetAlbum(in_album):
    tracks = sp.album_tracks(in_album['uri'])
    
    songs = []
    threads = []
    que = queue.Queue()
    print(len(tracks))
    for i in range(len(tracks)):
        track = tracks['items'][i]
        t = threading.Thread(target=lambda q, arg1: q.put(GetSong(track)), args=(que,track,))
        threads.append(t)
        t.start()
        #songs.append(GetSong(track))
    for t in threads:
        t.join()
        songs.append(que.get())
    album = Album(in_album, songs)
    return album

def GetArtist(artist):
    sp_albums = sp.artist_albums(artist['uri'])
    albums = []
    for i in range(len(sp_albums['items'])):
        if sp_albums['items'][i]['name'] not in albums:
            albums.append(GetAlbum(sp_albums['items'][i]))
    
    return Artist(artist, albums) 


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

name = "Lumineers"
result = sp.search(name, limit=1, type='artist')
print(result['artists']['items'][0]['name'])
artist = GetArtist(result['artists']['items'][0])
average = GetAverage(artist.albums[0].songs, artist.name)
GraphSongFeatures(average)
#sp_album = result['albums']['items'][0]
#album = GetAlbum(sp_album)
#average = GetAverage(album.songs, album.name)
#GraphSongFeatures(average)
#for song in album.songs:
#    print(song.name)
