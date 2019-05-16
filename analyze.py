from music.album import Album
from music.song import Song
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
    plt.title(song.name +' Features')
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

def GetAlbum(name):
    result = sp.search(name)
    sp_album = result['tracks']['items'][0]['album']
    tracks = sp.album_tracks(sp_album['uri'])
    
    songs = []
    threads = []
    que = queue.Queue()

    for i in range(len(tracks)):
        track = tracks['items'][i]
        #t = threading.Thread(target=lambda q, arg1: q.put(GetSong(track)), args=(que,track,))
        #threads.append(t)
        #t.start()
        #print("thread # started")
        songs.append(GetSong(track))
    #for t in threads:
     #   songs.append(t.join())
      #  print("thread stopped")
    album = Album(sp_album, songs)
    return album

album = GetAlbum("Cleopatra")
print(album.name)
print(album.release_date)
print(album.release_date_precision)
print(album.artist)
print(album.songs[0].name)
