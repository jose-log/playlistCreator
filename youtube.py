
import urllib.request
import urllib.parse
import urllib.error

# Should be able to use urllib to build the google API request

url = ''

data = urllib.request.urlopen(url)
data = data.decode()


