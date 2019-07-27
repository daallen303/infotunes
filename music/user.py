from credentials import SpotifyManager

spotify_manager = SpotifyManager()
sp = spotify_manager.GetCertified()

# This class allows for artists to be used multiple times if they are in more than one category for a user's top artist
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

class User:
    
    def __init__(self, user_name, spot):
        self.name = user_name
        
        user_info = sp.user(self.name)
        self.display_name = user_info['display_name']
        
        playlist_info = sp.user_playlists(self.name)

        # Placeholder for all information on top tracks 
        lr_top_tracks = []
        mr_top_tracks = [] 
        sr_top_tracks = []

        lr_top_tracks = spot.current_user_top_tracks(limit=20, time_range='long_term')
        mr_top_tracks = spot.current_user_top_tracks(limit=20, time_range='medium_term')
        sr_top_tracks = spot.current_user_top_tracks(limit=20, time_range='short_term')

        # Users top tracks
        self.lr_top_track_names = []
        self.mr_top_track_names = []
        self.sr_top_track_names = []
        
        for i in range(len(lr_top_tracks['items'])):
            self.lr_top_track_names.append(lr_top_tracks['items'][i]['name'])
            self.mr_top_track_names.append(mr_top_tracks['items'][i]['name'])
            self.sr_top_track_names.append(sr_top_tracks['items'][i]['name'])
        
        # Users top Artists
        
        self.lr_artist_names = []
        self.mr_artist_names = []
        self.sr_artist_names = []
        
        self.all_top_artists = []
        self.all_top_artists_uri = []
        
        # Placeholders for all information on Top artists
        lr_top_artists = []
        mr_top_artists = [] 
        sr_top_artists = []
        
        # Getting information about top artists
        lr_top_artists = spot.current_user_top_artists(limit=20, time_range='long_term')
        mr_top_artists = spot.current_user_top_artists(limit=20, time_range='medium_term')
        sr_top_artists = spot.current_user_top_artists(limit=20, time_range='short_term')
        
        for i in range(len(lr_top_artists['items'])):
            self.all_top_artists.append(TopArtist(lr_top_artists['items'][i]['name'],i))
            self.all_top_artists_uri.append(lr_top_artists['items'][i]['uri'])
        for i in range(len(lr_top_artists['items'])):
            if mr_top_artists['items'][i]['uri'] in self.all_top_artists_uri:
                self.all_top_artists[self.all_top_artists_uri.index(mr_top_artists['items'][i]['uri'])].SetMrSpot(i)
            else:
                self.all_top_artists_uri.append(mr_top_artists['items'][i]['uri'])
                self.all_top_artists.append(TopArtist(mr_top_artists['items'][i]['name'], -1))
                self.all_top_artists[-1].SetMrSpot(i)
            if sr_top_artists['items'][i]['uri'] in self.all_top_artists_uri:
                self.all_top_artists[self.all_top_artists_uri.index(sr_top_artists['items'][i]['uri'])].SetSrSpot(i)
            else:
                self.all_top_artists_uri.append(sr_top_artists['items'][i]['uri'])
                self.all_top_artists.append(TopArtist(sr_top_artists['items'][i]['name'], -1))
                self.all_top_artists[-1].SetSrSpot(i)

        for i in range(20):

            # Get the index in all_top_artists of the artist at spot 1-20 for long, medium, and short range by using their uri
            lr_index = self.all_top_artists_uri.index(lr_top_artists['items'][i]['uri'])
            mr_index = self.all_top_artists_uri.index(mr_top_artists['items'][i]['uri'])
            sr_index = self.all_top_artists_uri.index(sr_top_artists['items'][i]['uri'])
            
            mr_artist = self.all_top_artists[mr_index]
            sr_artist = self.all_top_artists[sr_index]
            
            # initialize to be * for a new artists that isn't in the long range but is in med or short
            mr_change = sr_change = " *"
            
            # Get the difference of an artists spot in long range list and in medium range list
            if mr_artist.lr_spot != -1:
                diff = mr_artist.lr_spot - mr_artist.mr_spot
                if diff > 0:
                    mr_change = " +" + str(diff)
                else:
                    mr_change = " " + str(diff)
                            
            # Get the difference of an artists spot in long range list and in short range list
            if sr_artist.lr_spot != -1:
                diff = sr_artist.lr_spot - sr_artist.sr_spot
                if diff > 0:
                    sr_change = " +" + str(diff)
                else:
                    sr_change = " " + str(diff)
            
            self.lr_artist_names.append(self.all_top_artists[lr_index].name)
            self.mr_artist_names.append(self.all_top_artists[mr_index].name+mr_change)
            self.sr_artist_names.append(self.all_top_artists[sr_index].name+sr_change)



# Class for storing info on a user
        
