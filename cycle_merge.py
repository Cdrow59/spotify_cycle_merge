import os
import sys
import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict



# Define your Spotify client credentials
client_id = "09cfdea368b64101b4c4fcc3508ab23f"
client_secret = "44a2130e4810455eb08c6a265e54e84c"
redirect_uri = 'http://localhost:8000/callback'


# Create a Spotify client instance with authorization and custom cache
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-modify-public',cache_path=".cache"))

#Define Functions
def custom_sort(target):
    #define result
    result = []
    random.seed(a=seed ,version=2)
    # Loop through each key in the dictionary
    loop = True
    while loop == True:
        for key in target:
            # Check if the list associated with the key is not empty
            if target[key]:
                # Randomly choose a value from the list
                random_value = random.choice(target[key])
                result.append(random_value)
                # Remove the chosen value from the list
                target[key].remove(random_value)
            else:
                loop = False
                break
    return result

#Configure Script
setseed = None

playlists = [
    "spotify:playlist:5DDg9WcDDC54z69Y51KSmW",
    "spotify:playlist:0w4vurwPbF5sv6tUEBEsWK",
    "spotify:playlist:0fP2GmLGb5FCS4GvBiS3lu",
    "spotify:playlist:3mybWjdM3iddZDoB00XGJs"
]

#Set Seed logic
if setseed is None:
    seed = random.randrange(sys.maxsize)
    rng = random.Random(seed)
    print("Seed was:", seed)
else:
    seed = setseed
    print("Seed was:", seed)
    
# Initialize an empty dictionary to store the data
data = {}

# Initialize an list dictionary to store sorted track ids
track_ids = []

# Initialize a set to store all added track IDs
added_track_ids = set()

# Iterate over playlists
print("Please wait this may take a while!")
for index, playlist in enumerate(playlists):
    
    # Retrieve the first page of tracks in the playlist
    results = sp.playlist_tracks(playlist)

    playlist_tracks = results['items']
    
    # Iterate through additional pages if available
    while results['next']:
        results = sp.next(results)
        playlist_tracks.extend(results['items'])
    
    # Process the retrieved tracks
    for item in playlist_tracks:
        track = item['track']
        track_id = track['id']
        
        if track_id is None or track_id in added_track_ids:  # Check if the track ID is None or already in the set
            continue  # Skip processing if it meets the condition
        
        # Check if the index is already a key in the dictionary
        if index in data:
            # If the index exists, append the track_id to the list of track_ids
            data[index].append(track_id)
            # Add the track ID to the set of added track IDs
            added_track_ids.add(track_id)
        else:
            # If the index does not exist, create a new key-value pair
            data[index] = [track_id]
            # Add the track ID to the set of added track IDs
            added_track_ids.add(track_id)
            
#Define Copy
datacopy = data
#Call Functions
track_ids = custom_sort(datacopy)

#Chunking Setup
a_list = track_ids
chunked_list = list()
chunk_size = 10000
n_chunks = 0

#Playlist Addition Setup
playlist_ids = []

#Handle Playlists Bigger Than 10,000
for i in range(0, len(a_list), chunk_size):
    chunked_list.append(a_list[i:i+chunk_size])
    n_chunks += 1
        
for index, sublist in enumerate(chunked_list):
    # Create a new playlist(s)
    if index == 0:
        playlist_name = 'Merged Playlist'
    else:
        part_number = index+1
        playlist_name = 'Merged Playlist' + ' Part ' + str(part_number)
    playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, public=True)
    playlist_ids.append(playlist['id'])


    # Add the tracks to the playlist(s) in batches of 100
    for i in range(0, len(sublist), 100):
        batch = sublist[i:i+100]
        sp.playlist_add_items(playlist_ids[index], batch)

print("Done please check your Spotify playlists")

