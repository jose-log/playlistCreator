#!/usr/bin/env python3

# Spotify API: https://developer.spotify.com/documentation/web-api/
# OAuth doc: https://oauth.net/articles/authentication/
#
# This script implements all the basic functionality to interface with the
# spotify API using the Requests module and the documentation given in
# the API developers page.
#
# It does NOT implement a direct OAuth authentication procedure, but instead
# it uses the web API token generator to generate an access token and use it
# to access user's data.
#
# Direct OAuth implementation was performed in a separate script, where an
# HTTP server is built and listens to the OAuth redirection scheme

# Requests module: https://requests.readthedocs.io/en/master/
import requests
import json

import spotifyOAuth as oauth

# GLOBAL VARIABLES!
oauth_code = ''		# Overwritten when getting authorization
oauth_token = ''	# Overwritten when getting authorization

PLAYLISTS_FILE = 'spotify_pl.txt'

###############################################################################
# 	POST REQUESTS
###############################################################################

def create_new_playlist(pl_name):

	usr_id = get_user_id()
	if usr_id is None:
		print('ERROR. Could not get User ID')
		exit()

	endpoint = 'https://api.spotify.com/v1/users/{}/playlists'.format(usr_id)

	parameters = {
		'name': pl_name,
		'description': 'Liked Youtube Videos',
		'public': True
	}
	head = {
		'Accept':'application/json',
		'Content-Type': 'application/json',
		'Authorization': 'Bearer {}'.format(oauth_token)
	}
	payload = json.dumps(parameters)

	print('  - Creating new playlist')
	response = requests.post(endpoint, data=payload, headers=head)
	response_json = response.json()

	try:
		out = response_json['id']
		print('  > New playlist \"' + pl_name + '\" created: ' + out)
	except:
		# print(json.dumps(response_json, sort_keys=True, indent=4))
		print('ERROR:', response_json['error']['status'])
		print('message:', response_json['error']['message'])
		out = response_json['error']['status']

	return out

#******************************************************************************
def insert_into_playlist(pl_id, tracks):

	endpoint = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(pl_id)

	while True:

		if len(tracks) > 100:
			next_array = tracks[100:]
			tracks = tracks[:100]
		else:
			next_array = []

		parameters = {
			'uris': tracks
		}
		head = {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'Authorization': 'Bearer {}'.format(oauth_token)
		}
		payload = json.dumps(parameters)

		print('Adding item to playlist...')
		response = requests.post(endpoint, data=payload, headers=head)
		response_json = response.json()

		try:
			# playlist id
			out = response_json['snapshot_id']
		except:
			print(json.dumps(response_json, sort_keys=True, indent=4))
			print('ERROR:', response_json['error']['status'])
			print('message:', response_json['error']['message'])
			out = response_json['error']['status']

		if len(next_array) is 0:
			break
		else:
			tracks = next_array;

	return 0

###############################################################################
# 	GET REQUESTS
###############################################################################

def get_user_id():

	endpoint = 'https://api.spotify.com/v1/me'

	head = {
		'Accept':'application/json',
		'Content-Type':'application/json',
		'Authorization':'Bearer {}'.format(oauth_token)
	}

	print('  - Retrieving user ID...')
	response = requests.get(endpoint, headers=head)
	response_json = response.json()
	  
	usr = None
	try:
		usr = response_json['id']
		print('>> User ID: ', usr)
	except:
		# Dump JSON response to screen
		print(json.dumps(response_json, sort_keys=True, indent=4))
		print('ERROR:', response_json['error']['status'])
		print('message:', response_json['error']['message'])
		exit()

	return usr

#******************************************************************************
def retrieve_user_playlists():

	endpoint = 'https://api.spotify.com/v1/me/playlists'

	parameters = {
		'limit':'50',
		'offset':'0'
	}
	head = {
		'Accept':'application/json',
		'Content-Type':'application/json',
		'Authorization':'Bearer {}'.format(oauth_token)
	}

	print('  - Retrieving user playlists...')
	response = requests.get(endpoint, params=parameters, headers=head)
	response_json = response.json()
    
	try:
		print('  > Playlists Count: ', response_json['total'])
	except:
		# Dump JSON response to screen
		# print(json.dumps(response_json, sort_keys=True, indent=4))
		print('ERROR:', response_json['error']['status'])
		print('message:', response_json['error']['message'])
		exit()

	c = 0
	pl = {}
	for i in response_json['items']:
	    # Store data into the data base
	    print(' > Playlist {}: {} | Songs = {} | ID: {}'.format(c + 1, i['name'], i['tracks']['total'], i['id']))
	    pl[i['name']] = i['id']
	    c += 1

	# Back up the filtered playlist names
	fh = open(PLAYLISTS_FILE, 'w')
	for i,j in pl.items():
		fh.write(i + ',' + j + '\n')
	fh.close()
	
	return pl

#******************************************************************************
def search_catalog(track, artist):

	endpoint = 'https://api.spotify.com/v1/search'

	parameters = {
		'q':'track:{} artist:{}'.format(track, artist),
		'type':'track',
		'limit':'1'
	}
	head = {
		'Accept':'application/json',
		'Content-Type':'application/json',
		'Authorization':'Bearer {}'.format(oauth_token)
	}

	response = requests.get(endpoint, params=parameters, headers=head)
	response_json = response.json()

	try:
		songs = response_json['tracks']['items']
		# only use the first song, if results are available
		if len(songs) is not 0:
			out = songs[0]['uri']
		else:
			out = None
	except:
		# print(json.dumps(response_json, sort_keys=True, indent=4))
		print('ERROR:', response_json['error']['status'])
		print('message:', response_json['error']['message'])
		out = None
		
	return out

###############################################################################
# 	MISC
###############################################################################

def get_authorization():

	global oauth_code
	global oauth_token
	
	oauth_token = oauth.request_valid_token()
	
	if oauth_token is None:
		print('  - Requesting new access token')
		oauth_code = oauth.get_authorization_code()
		oauth_token = oauth.request_access_token(oauth_code)

#******************************************************************************
def read_user_playlists():

	pl = {}

	try:
		fh = open(PLAYLISTS_FILE)
		for line in fh:
			line = line.rstrip('\n')
			x = line.split(',')
			pl[x[0]] = x[1]
		fh.close()
	except:
		pl = retrieve_user_playlists()

	return pl

#******************************************************************************
def create_spotify_playlist(name):

	pl = retrieve_user_playlists()
	# pl = read_user_playlists()

	if name not in pl.keys():
		pl_id = create_new_playlist(name)
	else:
		print('  - Youtube playlist already exists')
		pl_id = pl[name]

	return pl_id
	