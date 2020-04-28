
# Spotify API: https://developer.spotify.com/documentation/web-api/
# OAuth doc: https://oauth.net/articles/authentication/

# Requests module: https://requests.readthedocs.io/en/master/
import requests
import json

from spotify_secrets import spotify_oauth_token as oauth_token
from spotify_secrets import spotify_user_id as usr_id
from spotify_secrets import client_app_id as app_id
from spotify_secrets import client_app_secret as app_secret

serviceurl = 'https://api.spotify.com/v1'
authurl = 'https://accounts.spotify.com/authorize'

def create_playlist():
    
    request_body = json.dumps({
        "name": "Youtube Liked Vids",
        "description": "All Liked Youtube Videos",
        "public": True
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(
        spotify_user_id)
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    response_json = response.json()

    # playlist id
    return response_json

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
	response = requests.get(endpoint, params=parameters, headers=head)

	response_json = response.json()
    
	# Dump JSON response to screen
	# print(json.dumps(response_json, sort_keys=True, indent=4))
	print('Playlists Count: ', response_json['total'])

	c = 0
	pl = []
	for i in response_json['items']:
	    # Store data into the data base
	    print(' > Playlist {}: {} | Songs = {} | ID: {}'.format(c + 1, i['name'], i['tracks']['total'], i['id']))
	    pl.append(i['name'])
	    c += 1

	# Back up json response
	fh = open('spotify_pl.json', 'w')
	json.dump(response_json, fh, sort_keys=True, indent=4)
	fh.close()
	# Back up the filtered playlist names
	fh = open('spotify_pl.txt', 'w')
	for i in pl:
		fh.write(i + '\n')
	fh.close()
	
	return pl

def read_user_playlists():

	pl = []
	fh = open('spotify_pl.txt')
	for line in fh:
		pl.append(line)
	fh.close()

	return pl

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

	if new_playlist not in pl:
		print('Creating new Youtube playlist')
	else:
		print('Youtube playlist already exists')
