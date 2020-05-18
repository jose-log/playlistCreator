
import urllib.request
import urllib.parse
import urllib.error

# Should be able to use urllib to build the google API request

nxtPage = None

serviceurl = 'https://www.googleapis.com/youtube/v3/videos?'
api_key = None
parms = dict()
parms['part'] = 'snippet,contentDetails'
parms['myRating'] = 'like'
parms['maxResults'] = 50
parms['fields'] = 'items(id,contentDetails(duration),snippet(title))'
parms['pageToken'] = nxtPage

###################################################

GET https://www.googleapis.com/youtube/v3/videos?
	part=snippet%2CcontentDetails
	&maxResults=50
	&myRating=like
	&fields=items(id%2CcontentDetails(duration)%2Csnippet(title))
	&key=[YOUR_API_KEY] HTTP/1.1

Authorization: Bearer [YOUR_ACCESS_TOKEN]
Accept: application/json

###################################################

curl \
  'https://www.googleapis.com/youtube/v3/videos?	\
  	part=snippet%2CcontentDetails	\
  	&maxResults=50	\
  	&myRating=like	\
  	&fields=items(id%2CcontentDetails(duration)%2Csnippet(title))	\
  	&key=[YOUR_API_KEY]' \
  --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
  --header 'Accept: application/json' \
  --compressed

###################################################

url = serviceurl + urllib.parse.urlencode(parms)

data = urllib.request.urlopen(url)
data = data.decode()

