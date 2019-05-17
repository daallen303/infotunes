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

def GraphKey(songs):
    C=Db=D=Eb=E=F=Gb=G=Ab=A=Bb=B=0
    for song in songs:
        if song.key == 0:
            C += 1
        if song.key == 1:
            Db += 1
        if song.key == 2:
            D += 1
        if song.key == 3:
            Eb += 1
        if song.key == 4:
            E += 1
        if song.key == 5:
            F += 1
        if song.key == 6:
            Gb += 1
        if song.key == 7:
            G+= 1
        if song.key == 8:
            Ab += 1
        if song.key == 9:
            A += 1
        if song.key == 10:
            Bb += 1
        if song.key == 11:
            B += 1
    labels = ['C','Db','D','Eb','E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    sizes = [C,Db,D,Eb,E,F,Gb,G,Ab,A,Bb, B]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','blue', 'orange', 'pink','yellow', 'purple', 'red', 'green', 'grey']

    delete_indexes = []
    for i in range(len(sizes)):
        if sizes[i] == 0:
            delete_indexes.append(i)
    count = 0
    for i in delete_indexes:
            del sizes[i-count]
            del labels[i-count]
            del colors[i-count]
            count+=1
    print(len(sizes))
    explode = (0,0.1,0,0,0,0)
    plt.title("Song Keys for the Lumineers Cleopatra")    
    plt.pie(sizes, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%')
    
    plt.axis('equal')
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
    print(len(tracks['items']))
    for i in range(len(tracks['items'])):
        track = tracks['items'][i]
        t = threading.Thread(target=lambda q, arg1: q.put(GetSong(track)), args=(que,track,))
        threads.append(t)
        t.start()
        songs.append(GetSong(track))
    for t in threads:
        t.join()
        songs.append(que.get())
    album = Album(in_album, songs)
    return album

def GetArtist(artist):
    sp_albums = sp.artist_albums(artist['uri'])
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

name = "Stairway to Heaven"
result = sp.search(name, limit=1, type='track')
GetSong(result['tracks']['items'][0])

#print(result['artists']['items'][0]['name'])
#artist = GetArtist(result['artists']['items'][0])
#average = GetAllSongsFromArtist(artist)
#GraphSongFeatures(average)
#sp_album = result['albums']['items'][0]
#album = GetAlbum(sp_album)
#GraphKey(album.songs)
#average = GetAverage(album.songs, album.name)
#GraphSongFeatures(average)
#for song in album.songs:
#    print(song.name)
