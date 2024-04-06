import os
import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict



# Define your Spotify client credentials
client_id = "09cfdea368b64101b4c4fcc3508ab23f"
client_secret = "44a2130e4810455eb08c6a265e54e84c"
redirect_uri = 'http://localhost:8000/callback'

filename = (os.path.splitext(os.path.basename(__file__))[0])
cache_path = ("C:\\Users\\Clayton\\AppData\\Local\\Temp\\vscode\\" +filename+ ".cache")

# Create a Spotify client instance with authorization and custom cache
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-modify-public',cache_path=cache_path))

#Define Functions
def custom_sort(lst):
    # Separate the list into groups based on the first element of each tuple
    grouped = {}
    for item in lst:
        index = item[0]
        grouped.setdefault(index, []).append(item)

    # Create a list to store the sorted result
    sorted_list = []

    # Determine the minimum length among the groups
    min_len = min(len(grouped[index]) for index in grouped)

    # Alternate between groups and extend the sorted list
    for i in range(min_len):
        for index in sorted(grouped):
            sorted_list.append(grouped[index][i])

    return sorted_list

def random_sort(arr):
    n = len(arr)
    for i in range(n):
        j = random.randint(0, n-1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def extract_second_elements(list_of_tuples):
    return [tup[1] for tup in list_of_tuples]

shuffle = True
playlists = [
    "spotify:playlist:0fP2GmLGb5FCS4GvBiS3lu",
    "spotify:playlist:0w4vurwPbF5sv6tUEBEsWK",
    "spotify:playlist:5DDg9WcDDC54z69Y51KSmW"
]
data = []
print("PLease wait this may take a while!")
for index, playlist in enumerate(playlists):
    # Retrieve the playlist tracks
    tracks = sp.playlist_tracks(playlist)

    # Extract track names and artists from the response
    track_info = []
    for item in tracks['items']:
        track = item['track']
        track_id = track['id']
        data.append((index, track_id))

# Shuffle Logic and Calling Sorts
if shuffle == True:
    rand = random_sort(data)
    sort = custom_sort(rand)
else:
    sort = custom_sort(data)

#Remove First/Tuple element after sorting
track_uris = extract_second_elements(sort)

#Chunking Setup
a_list = track_uris
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

