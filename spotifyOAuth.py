#!/bin/env python3

# This script implements direct OAuth authentication protocol based on the
# Spotify web API documentation. The Authentication process uses the
# Authorization Code Flow, which only requires from the user to authorize
# the client application only once using the web browser
#
# The end result is an access token that can later be included in the API
# methods to access the users' data

# Web communication modules
import requests
import urllib.request
import urllib.parse

# Browser and server modules
import webbrowser
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

# Utility modules
import json
import base64
import time
import random

# Secrets modules
from secrets_spotify import client_id
from secrets_spotify import client_secret

# Authorization endpoints:
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = 'http://localhost:9090'

CACHE_PATH = './.cache-token'

SCOPES = 'user-read-private playlist-read-private playlist-modify-public playlist-modify-private'

#******************************************************************************
# RequestHandler
# Extended class from BaseHTTPRequestHandler used to handle the spotify
# authorization response and get the authorization code.
#
# https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.handle_one_request
#
class RequestHandler(BaseHTTPRequestHandler):

	# GET method handler:
	def do_GET(self):
		query_s = urllib.parse.urlparse(self.path).query
		form = dict(urllib.parse.parse_qsl(query_s))

		self.send_response(200)
		self.send_header("Content-Type", "text/html")
		self.end_headers()

		if "code" in form:
			self.server.auth_code = form["code"]
			self.server.state = form["state"]
			self.server.error = None
			status = "successful"
		elif "error" in form:
			self.server.error = form["error"]
			self.server.auth_code = None
			status = "failed ({})".format(form["error"])
		else:
			self._write("<html><body><h1>Invalid request</h1></body></html>")
			return

		self._write("""	<html>
							<body>
								<h1>Authentication status: {}</h1>
								This window can be closed.
								<script>
									window.close()
								</script>
							</body>
						</html>""".format(status))

	def _write(self, text):
		return self.wfile.write(text.encode("utf-8"))

#******************************************************************************
# Request authorization to access data
# The requests module could be used to send a GET request to the authoriza-
# tion server, nevertheless, user authentication is required, thus, the
# web browser must be used to ask the user for login and authorization
#
def get_authorization_code():
	
	code = None
	redirect_port = 9090
	print('  > Creating Local Server in port:', str(redirect_port))
	server = start_local_http_server(redirect_port)

	state = generate_random_string(20)
	print('  - Random state string: ' + state)
	url = build_authorize_url(state)
	print('  > OAuth Authorization URL:', url)
	try:
		webbrowser.open(url)
		print('  - Authentication URL opened in your browser:', AUTH_URL)
	except webbrowser.Error:
		print('  - Please navigate here:', url)
	
	print(' >> Handling request')
	server.handle_request()		# wait for authorization endpoint response

	if server.auth_code is not None:
		code = server.auth_code
		if server.state.strip() != state:
			print('ERROR: response state don\'t match')
			print(server.state)
	elif server.error is not None:
		print('  - Received error from OAuth server: {}'.format(server.error))
		exit()
	else:
		print('  - Server listening on localhost has not been accessed')
		exit()

	return code

#******************************************************************************
# Request refresh and access tokens
# This time, no user interaction through the browser is needed, thus, the
# POST request is handled using Requests module
#
def request_access_token(code):

	token = None
	payload = {
		'redirect_uri': REDIRECT_URI,
		'code': code,
		'grant_type': 'authorization_code',
	}
	headers = make_authorization_headers()

	response = requests.post(TOKEN_URL, data=payload, headers=headers)

	if response.status_code != 200:
		print('ERROR. Token request failed')
		print(response)
		exit()

	token_info = response.json()
	# Compute time value for token expiration date
	token_info['expires_at'] = int(time.time()) + token_info.get('expires_in')
	save_token_info(token_info)
	
	return token_info.get('access_token')


#******************************************************************************
def generate_random_string(length):
	
	rand = ''
	universe = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
	for i in range(length):
		rand += universe[random.randint(0, len(universe) - 1)]

	return rand

#******************************************************************************
def start_local_http_server(port, handler=RequestHandler):
	
	server = HTTPServer(("127.0.0.1", port), handler)
	server.allow_reuse_address = True
	server.auth_code = None
	server.error = None
	return server

#******************************************************************************
def build_authorize_url(state):
	# Gets the URL to use to authorize this app
	payload = {
		'response_type':'code',
		'client_id':client_id,
		'state':state,
		'scope':SCOPES,
		'redirect_uri':REDIRECT_URI,
	}

	urlparams = urllib.parse.urlencode(payload)

	return '{}?{}'.format(AUTH_URL, urlparams)

#******************************************************************************
def make_authorization_headers():
	# This method encodes the header, nevertheless the API allows to send these
	# parameters as part of the POST request body.
	auth_header = (client_id + ':' + client_secret).encode('ascii')
	auth_header = base64.b64encode(auth_header)
	return {'Authorization': 'Basic {}'.format(auth_header.decode('ascii'))}

#******************************************************************************
def save_token_info(token_info):
	try:
		f = open(CACHE_PATH, 'w')
		f.write(json.dumps(token_info))
		f.close()
		return True
	except:
		print('Couldn\'t write token to cache at: {}'.format(CACHE_PATH))
		return False

#******************************************************************************
def get_cached_token():

	token_info = None
	print('  - Extracting Spotify cached token')

	try:
		f = open(CACHE_PATH)
		token_info_string = f.read()
		f.close()
		token_info = json.loads(token_info_string)

	except:
		print('ERROR. Opening {} failed'.format(CACHE_PATH))

	return token_info

#******************************************************************************
def is_token_expired(token_info):

	now = int(time.time())
	# if expiration time is less than a minute
	return token_info['expires_at'] - now < 60

#******************************************************************************
def refresh_access_token(refresh_token):

	if refresh_token is None:
		print('  - WARNING: Invalid refresh token')
		return None

	payload = {
		'refresh_token': refresh_token,
		'grant_type': 'refresh_token',
	}
	headers = make_authorization_headers()

	response = requests.post(TOKEN_URL, data=payload, headers=headers)

	if response.status_code != 200:
		print('ERROR. Refresh token request failed')
		exit()

	token_info = response.json()
	# Compute time value for token expiration date
	token_info['expires_at'] = int(time.time()) + token_info.get('expires_in')
	if 'refresh_token' not in token_info:
		token_info['refresh_token'] = refresh_token
	save_token_info(token_info)
	
	return token_info.get('access_token')

#******************************************************************************
def request_valid_token():

	token = None
	token_info = get_cached_token()
	
	if token_info is None:
		print('WARNING. No cached token was found')
	else:
		if is_token_expired(token_info):
			print('  - Cached token expired. Refreshing access token')
			token = refresh_access_token(token_info.get('refresh_token'))
		else:
			print('  - Cached token VALID')
			token = token_info.get('access_token')

	return token