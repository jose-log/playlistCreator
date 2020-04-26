
# Spotify API: https://developer.spotify.com/documentation/web-api/
# Base address: https://api.spotify.com/v1

# Client ID: 253c6a6d9c6b44e6bd1cb5c9c3bb690b
# Client secret: 96f2900e96e24976a13f39bd2929a3b2
Want to showcase your
app on our website?


import urllib.request
import urllib.parse
import urllib.error

serviceurl = 'https://api.spotify.com/v1'

parms = dict()
parms['part'] = 'snippet,contentDetails'
parms['myRating'] = 'like'
parms['maxResults'] = 50
parms['fields'] = 'items(id,contentDetails(duration),snippet(title))'
parms['pageToken'] = nxtPage