
# Miscellaneous
import json

# SPOTIPY-related
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

# Secrets-related
from spotify_secrets import client_app_id as client_id
from spotify_secrets import client_app_secret as client_secret
from spotify_secrets import spotify_user_id as username

#############################################################
#
# Steps:
# 1. Retrieve all user playlists: current_user_playlists(limit=50, offset=0
# 2. Look for the Youtube like vids playlist
# 3. If non-existent, create it. If existent, get the ID.
# 4. Based on the videos_dump.json files, read them and look for the songs in spotify
# 5. If songs exist, add them to the playlist.


def get_authentication(scope=None):

	redirect_uri = 'http://localhost:9090'

	print('> Getting OAuth authentication')
	token = util.prompt_for_user_token(redirect_uri=redirect_uri, scope=scope)

	 if token is None:
	     print('Can\'t get token for', username)
	     exit()

	print('  Authentication successful')
	sp = spotipy.Spotify(auth=token)

	return sp

def download_user_playlists(sp):

	print('> Downloading playlists')
	playlists = sp.user_playlists(username)

	usr_pl = {}
	for playlist in playlists['items']:
	    print(playlist['name'], playlist['id'])
	    usr_pl[playlist['name']] = playlist['id']
	print(username, 'playlists retrieved')

	return usr_pl

def create_new_playlist(playlist):

	scope = 'playlist-modify-public'
	sp = get_authentication(scope)
	sp.user_playlist_create(username, playlist)

def add_tracks_to_playlist(playlist, tracks):

	scope = 'playlist-modify-public'
	sp = get_authentication(scope)
	sp.user_playlist_add_tracks(username, playlist, tracks)

###############################################################################
#   					   M A I N   P R O G R A M
###############################################################################

if __name__ == '__main__':
    
	sp = get_authentication()
	usr_pl = download_user_playlists(sp)

	new_playlist = 'Youtube Liked Vids'
	if new_playlist not in usr_pl.keys():
		print('WARNING!: Youtube playlist non-existent')
		print('> Creating Spotify playlist')
		create_new_playlist(new_playlist)
		# Downolad again playlists to get New Playlist URI
		usr_pl = download_user_playlists(sp)
	else:
		print('WARNING!: Youtube playlist already exists')
		print('  ', new_playlist, 'ID:', usr_pl[new_playlist])

	test_array = []
	test_array.append(('Hillsong','Another in the fire'))
	test_array.append(('David Crowder','B Collision'))
	test_array.append(('Kike Pavon','Torpe Corazón'))
	test_array.append(('Un Corazón','la calle'))
	test_array.append(('Ecclesia','Excellence'))

	track_ids = []
	# shows related artists for the given seed artist
	for item in test_array:

		result = sp.search(q='track:' + item[1] + ' artist:' + item[0], type='track')
		try:
		    name = result['tracks']['items'][0]['name']
		    uri = result['tracks']['items'][0]['uri']
		    artist = result['tracks']['items'][0]['artists'][0]['name']
		    print(name + ' | ' + artist + ' | ' + uri)
		    track_ids.append(uri)
		except:
		    print("No results retrieved")
		    print(result)
		    exit()

	print('> Adding songs to playlist')
	add_tracks_to_playlist(usr_pl[new_playlist], track_ids)
	print(' > FINISHED!')