# In[1]:
# Needed imports
import numpy as np
import pandas as pd
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials

# In[2]:
# Spotify Credentials
SPOTIFY_CLIENT_ID='Client_ID'
SPOTIFY_CLIENT_SECRET='Client_Secret'
SPOTIFY_REDIRECT_URI='Redirect_URI'
SPOTIFY_USER_ID='User_ID' # id of user creating the playlist

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, 
                                                      client_secret=SPOTIFY_CLIENT_SECRET)
spotify = sp.Spotify(client_credentials_manager = client_credentials_manager)

# Playlists from spotify that focus around the Brazilian Zouk style of dance
playlist_titles = ['ZOUK',
                   'ZOUK FIRST DANCE',
                   'TOP ZOUK FIRST DANCE',
                   'BEST ZOUK FIRST DANCE',
                   'ZOUK WEDDING FIRST',
                   'BEST ZOUK',
                   'TOP ZOUK',
                   'ZOUK DANCE',
                   'MODERN ZOUK',
                   'FIRST DANCE']

# In[3]:
# Gather playlists from Spotify
playlists = []

# Search spotify for the playlists in playlist_titles
# Saves the results in playlists, or prints the name of the playlist search for reference if empty
for name in playlist_titles:
    results = spotify.search(q='playlist:' + name, type='playlist')
    items = results['playlists']['items']
    for i in range(0, len(items)):
        try:
            playlists.append([items[i]['uri']]) 
        except:
            print(name)

# Identified 45 playlists
print('Identified '+str(len(playlists))+' playlists')

# In[4]:
# Gather tracks from the playlists
tracks = []

# For each playlist identified, saves the track uri in tracks
for value in range(0, len(playlists)):
    uri = playlists[value][0]
    results = spotify.playlist_tracks(uri)
    for track in range(0, len(results)):
        try:
            tracks.append(results['items'][track]['track']['uri']) # append the URIs of each playlist's tracks
        except:
            print(track)

# Identified 315 songs
print('Selected '+str(len(tracks))+' songs')

# In[5]:
# Add in target song if not present
target = 'Fever Michael Buble'
target = spotify.search(q='track:' + target, limit = 1, type='track')
tracks.append(target['tracks']['items'][0]['uri'])

# Cleaning out uris that do not match the proper 36 character format   
tracks = [i for i in tracks if len(i) == 36] 

# In[6]:
# Obtain audio features
features = pd.DataFrame()
for track_chunk in [tracks[i:i + 20] for i in range(0, len(tracks), 20)]:
    features = features.append(pd.DataFrame(spotify.audio_features(track_chunk)))

# Drop duplicates and reset index: 272 songs remaining
features.drop_duplicates(subset ="uri", keep = 'last', inplace = True)
features.reset_index(inplace=True,drop=True)
features.info()

# In[7]:
# Add the name and artist of the track
features['name'] = np.nan
features['artist'] = np.nan

for i in range (0, len(features)):
    features['name'][i] = spotify.track(features.uri[i])['name']
    features['artist'][i] = spotify.track(features.uri[i])['artists'][0]['name']

# In[8]:
# Verifying Target
features.name[len(features)-1] + ' by ' + features.artist[len(features)-1]

# In[9]:
# Save progress for modeling
features.to_csv('path\\First Dance.csv')




