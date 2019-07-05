class User:
    
    def __init__(self, user_name):
        self.name = user_name
        
        user_info = sp.user(self.name)
        self.display_name = user_info['display_name']
        
        playlist_info = sp.user_playlists(self.name)

        self.playlists = []
        for n in range(len(playlist_info['items'])):
            self.playlists.append(Playlist(playlist_info['items'][n]))

# Class for storing info on a user
