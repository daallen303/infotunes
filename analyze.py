from graph import Graph
from music.album import Album
from music.song import Song
from music.artist import Artist
from credentials import SpotifyManager 
from prettytable import PrettyTable
import spotipy.util as util
import spotipy
import sys
import time 

spotify_manager = SpotifyManager()
sp = spotify_manager.GetCertified()

class TopArtist:
    def __init__(self, name, lr_spot):
        self.name = name 
        self.lr_spot = lr_spot
        self.mr_spot = -1
        self.sr_spot = -1

    def SetMrSpot(self, mr_spot):
        self.mr_spot = mr_spot

    def SetSrSpot(self, sr_spot):
        self.sr_spot = sr_spot

def GetSong(track_uri=None):   
    if track_uri == None:
        song_name = input("Enter the song's name \n")
        artist_name = input("Enter the artist's name \n")
        # Also have a thing to enter the artists name
        query =  "artist:%"+artist_name+" track:%"+song_name
        result = sp.search(q=query, type='track')
        if len(result['tracks']['items']) > 0:
            print("Getting Information about "+song_name)
            track = sp.track(result['tracks']['items'][0]['uri'])
        else: 
            print("Sorry, the search for "+song_name+" by " +artist_name+" returned no results. Please check the spellong and try again.")
            return None
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
        query = "artist:%"+ artist_name +" album:%"+ album_name
        result = sp.search(q=query, type='album')
        if len(result['albums']['items'])>0:
            album = result['albums']['items'][0] 
        else :
            print("Nothing matched the search for "+album_name+" by "+artist_name+ ", please try again")
            return None
    tracks = sp.album_tracks(album['uri'])
    sp_album = sp.album(album['uri'])
    songs = []
    if full_info == True:
        print("Getting Information about the songs in "+album_name)
        for i in range(len(tracks['items'])):
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
    result = sp.search(q='artist:' + name, type='artist')
    if len(result['artists']['items']) > 0:
        artist = result['artists']['items'][0]
        print("Generating information about " + name)
    else:
        print("Sorry no artist matched the search for"+name+", please try again")
        return None
    sp_albums = sp.artist_albums(artist['uri'], limit=50)
    albums = []
    album_names = []
    top_tracks_name = []
    top_tracks_pop = []
    result = sp.artist_top_tracks(artist['uri'])
    for i in range(len(result['tracks'])):
        top_tracks_name.append(result['tracks'][i]['name'])
        top_tracks_pop.append(result['tracks'][i]['popularity'])
    print("\n Collecting information about albums by the "+name+":\n")
    for i in range(len(sp_albums['items'])):
        if sp_albums['items'][i]['type'] == 'album' and sp_albums['items'][i]['name'] not in album_names:
            print(sp_albums['items'][i]['name'])
            albums.append(GetAlbum(sp_albums['items'][i]))
            album_names.append(sp_albums['items'][i]['name'])
    return Artist(artist, albums, top_tracks_name, top_tracks_pop) 

def GraphArtist(artist):
    Graph.AlbumPopularityOverTime(artist)
    
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
    scope = 'playlist-modify-public user-read-email user-top-read user-library-read'
    try :
        token = util.prompt_for_user_token(username, scope)
    except :
        print("Couldn't find the username"+username+", please make sure it is correct")

    if token:
        spot = spotipy.Spotify(auth=token)
        spot.trace = False
        #saved_tracks = sp.current_user_saved_tracks()
        #print(saved_tracks)
        lr_top_artists = []
        lr_top_artists = spot.current_user_top_artists(limit=20, time_range='long_term')
        mr_top_artists = [] 
        mr_top_artists = spot.current_user_top_artists(limit=20, time_range='medium_term')
        sr_top_artists = []
        sr_top_artists = spot.current_user_top_artists(limit=20, time_range='short_term')
        
        all_top_artists = []
        all_top_artists_uri = []
        
        t = PrettyTable(["Spot", "All-time", "Medium-range", "Short-range"])
        for i in range(len(lr_top_artists['items'])):
            all_top_artists.append(TopArtist(lr_top_artists['items'][i]['name'],i))
            all_top_artists_uri.append(lr_top_artists['items'][i]['uri'])
        for i in range(len(lr_top_artists['items'])):
            if mr_top_artists['items'][i]['uri'] in all_top_artists_uri:
                all_top_artists[all_top_artists_uri.index(mr_top_artists['items'][i]['uri'])].SetMrSpot(i)
            else:
                all_top_artists_uri.append(mr_top_artists['items'][i]['uri'])
                all_top_artists.append(TopArtist(mr_top_artists['items'][i]['name'], -1))
                all_top_artists[-1].SetMrSpot(i)
            if sr_top_artists['items'][i]['uri'] in all_top_artists_uri:
                all_top_artists[all_top_artists_uri.index(sr_top_artists['items'][i]['uri'])].SetSrSpot(i)
            else:
                all_top_artists_uri.append(sr_top_artists['items'][i]['uri'])
                all_top_artists.append(TopArtist(sr_top_artists['items'][i]['name'], -1))
                all_top_artists[-1].SetSrSpot(i)
            
        for i in range(20):
            lr_index = all_top_artists_uri.index(lr_top_artists['items'][i]['uri'])
            mr_index = all_top_artists_uri.index(mr_top_artists['items'][i]['uri'])
            sr_index = all_top_artists_uri.index(sr_top_artists['items'][i]['uri'])
            
            mr_artist = all_top_artists[mr_index]
            sr_artist = all_top_artists[sr_index]

            mr_change = sr_change = " *"
            if mr_artist.lr_spot != -1:
                diff = mr_artist.lr_spot - mr_artist.mr_spot
                if diff > 0:
                    mr_change = " +" + str(diff)
                else:
                    mr_change = " " + str(diff)
                            
            if sr_artist.lr_spot != -1:
                diff = sr_artist.lr_spot - sr_artist.sr_spot
                if diff > 0:
                    sr_change = " +" + str(diff)
                else:
                    sr_change = " " + str(diff)

            t.add_row([str(i+1),all_top_artists[lr_index].name, all_top_artists[mr_index].name+mr_change, all_top_artists[sr_index].name+sr_change])
        
        t.align = 'l'
        t.align["Spot"] = 'r'
        print(t)

        lr_top_tracks = []
        lr_top_tracks = spot.current_user_top_tracks(limit=20, time_range='long_term')
        mr_top_tracks = [] 
        mr_top_tracks = spot.current_user_top_tracks(limit=20, time_range='medium_term')
        sr_top_tracks = []
        sr_top_tracks = spot.current_user_top_tracks(limit=20, time_range='short_term')
        
        t2 = PrettyTable(["Spot", "All-time", "Medium-range", "Short-range"])
        
        
        for i in range(len(lr_top_tracks['items'])):
            t2.add_row([str(i+1),lr_top_tracks['items'][i]['name'], mr_top_tracks['items'][i]['name'], sr_top_tracks['items'][i]['name']])
        t2.align = 'l'
        t2.align["Spot"] = 'r'
        print(t2)
    else:
        print("Can't get token for", username)
def GraphUser():
    print("hello")

def GetPlaylist():
    name = input("Please input the playlists name\n")
    result = sp.search(q='playlist:' + name, type='playlist')
            
def GraphPlaylist(songs):
    Graph.GraphPlaylist(songs)

print("\n\nWelcome to InfoTunes \nWhat would you like information about? \n") 
option = input("Type 'u' for user, 'a' for artist, 's' for song, 'al' for album, 'p' for playlist, 'q' to quit and exit \n")


while option != 'q':
    if option == 'a':
        artist = GetArtist()
        if artist != None:
            GraphArtist(artist)
    elif option == 's':
        song = GetSong()
        if song != None:
            GraphSong(song)
    elif option == 'al':
        album = GetAlbum(full_info=True)
        if album != None:
            GraphAlbum(album)
    elif option == 'p':
        playlist = GetPlaylist()
        GraphPlaylist(playlist.songs)
    elif option == 'u':
        user = GetUser()
        GraphUser()
    else:
        print("Value not understood, please enter a valid value") 
    option = input("Type 'u' for user, 'a' for artist, 's' for song, 'al' for album, 'p' for playlist, 'q' to quit and exit \n")






