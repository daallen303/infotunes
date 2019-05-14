import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 

class SpotifyManager:

    def __init__(self):
        self.client_id = "e2e1e1eca1bf4883a109f3d4a30b3400"
        self.client_secret = "ba975017397d4b13aad38f876b5b99ad"
        self.redirect_uri = "https://localhost/"

    def GetCertified(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id,client_secret=self.client_secret)

        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Class for making requests to Spotify
