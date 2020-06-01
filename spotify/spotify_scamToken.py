
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

from spotify_secrets import spotify_oauth_token as oauth_token
from spotify_secrets import spotify_user_id as usr_id
from spotify_secrets import client_app_id as app_id
from spotify_secrets import client_app_secret as app_secret

serviceurl = 'https://api.spotify.com/v1'
authurl = 'https://accounts.spotify.com/authorize'

###############################################################################
# 	POST REQUESTS
###############################################################################

def create_new_playlist(pl_name):

	endpoint = 'https://api.spotify.com/v1/users/{}/playlists'.format(usr_id)

	parameters = {
		"name": pl_name,
		"description": "Liked Youtube Videos",
		"public": True
	}
	head = {
		'Accept':'application/json',
		"Content-Type": "application/json",
		"Authorization": "Bearer {}".format(oauth_token)
	}
	payload = json.dumps(parameters)

	print('Creating new playlist...')
	response = requests.post(endpoint, data=payload, headers=head)
	response_json = response.json()

	try:
		# playlist id
		out = response_json['id']
		print('>>New playlist \"' + pl_name + '\" created:')
	except:
		print(json.dumps(response_json, sort_keys=True, indent=4))
		print('ERROR:', response_json['error']['status'])
		print('message:', response_json['error']['message'])
		out = response_json['error']['status']

	return out

def insert_into_playlist(pl_id, song_uri):

	endpoint = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(pl_id)
	
	parameters = {
		'uris':['{}'.format(song_uri)]
	}
	head = {
		'Accept':'application/json',
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
		print('>>Track \"' + song_uri + '\" added to \"' + pl_id + '\" playlist')
	except:
		print(json.dumps(response_json, sort_keys=True, indent=4))
		print('ERROR:', response_json['error']['status'])
		print('message:', response_json['error']['message'])
		out = response_json['error']['status']

	return 0

###############################################################################
# 	GET REQUESTS
###############################################################################

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

	print('Retrieving user playlists...')
	response = requests.get(endpoint, params=parameters, headers=head)
	response_json = response.json()
    
	try:
		print('>> Playlists Count: ', response_json['total'])
	except:
		# Dump JSON response to screen
		print(json.dumps(response_json, sort_keys=True, indent=4))
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

	# Back up json response
	fh = open('spotify_pl.json', 'w')
	json.dump(response_json, fh, sort_keys=True, indent=4)
	fh.close()
	# Back up the filtered playlist names
	fh = open('spotify_pl.txt', 'w')
	for i,j in pl.items():
		fh.write(i + ',' + j + '\n')
	fh.close()
	
	return pl

def search_catalog(track, artist):

	endpoint = 'https://api.spotify.com/v1/search'

	parameters = {
		'q':'track:{} artist:{}'.format(track, artist),
		'type':'track',
		'limit':'3'
	}
	head = {
		'Accept':'application/json',
		'Content-Type':'application/json',
		'Authorization':'Bearer {}'.format(oauth_token)
	}

	print('Searching in spotify catalog...')
	response = requests.get(endpoint, params=parameters, headers=head)
	response_json = response.json()

	try:
		songs = response_json["tracks"]["items"]
		# only use the first song
		out = songs[0]["uri"]
		print('Search FINISHED!')
	except:
		print(json.dumps(response_json, sort_keys=True, indent=4))
		print('ERROR:', response_json['error']['status'])
		print('message:', response_json['error']['message'])
		out = response_json['error']['status']
		
	return out

###############################################################################
# 	MISC
###############################################################################

def read_user_playlists():

	pl = {}
	fh = open('spotify_pl.txt')
	for line in fh:
		line = line.rstrip('\n')
		x = line.split(',')
		pl[x[0]] = x[1]
	fh.close()

	return pl

###############################################################################
# 	MAIN PROGRAM
###############################################################################

if __name__ == '__main__':
    
    # print(create_playlist())
    #j = get_spotify_uri('hallelujah','hillsong')
    #print(j)

	print('\n\rHello World!\n\r< SPOTIFY API INTERACTION >')

	download = None
	while download is None:
		x = input('Do you want to download your playlists? (Y/n)')
		if x in 'yY ':
			download = True
			break
		elif x in 'nN':
			download = False
			break
		elif x in 'qQ':
			exit()
		else:
			print('INVALID!')

	if download is True:
		pl = retrieve_user_playlists()
	else:
		pl = read_user_playlists()

	new_playlist = 'Youtube Liked Vids'

	if new_playlist not in pl.keys():
		print('Creating new Youtube playlist')
		pl_id = create_new_playlist(new_playlist)
	else:
		print('Youtube playlist already exists')
		pl_id = pl[new_playlist]

	track_uri = (search_catalog('Oceans','Hillsong'))
	insert_into_playlist(pl_id, track_uri)