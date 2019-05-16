from music.song import Song
from credentials import SpotifyManager 
import matplotlib.pyplot as plt 
import numpy as np

spotify_manager = SpotifyManager()
sp = spotify_manager.GetCertified()

name = "DMX"
result = sp.search(name)

artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
sp_album = sp.artist_albums(artist_uri ,album_type='album', limit=1)

sp_track = sp.album_tracks(sp_album['items'][0]['uri'])
track = sp_track['items'][0]
audio_analysis = sp.audio_analysis(track['uri'])
audio_features = sp.audio_features(track['uri'])
song = Song(track['name'], track['uri'],audio_features, audio_analysis)

print(song)

labels = ('danceability', 'speechiness', 'acousticness','energy', 'instrumentalness', 'liveness')
y_pos = np.arange(len(labels))
confidence = [song.danceability, song.speechiness, song.acousticness, song.energy, song.instrumentalness, song.liveness]

plt.bar(y_pos, confidence, align='center', alpha=.1, color='blue',linewidth=1)
plt.xticks(y_pos, labels)
plt.ylabel('Confidence')
plt.title(song.name +' Features')

plt.show()
