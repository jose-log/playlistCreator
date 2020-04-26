
import json

fh = open('videos_dump.json')

js = json.load(fh)

print('\n\n\r')
print(' > Results Per Page: {}'.format(js['pageInfo']['resultsPerPage']))
print(' > Total Results: {}'.format(js['pageInfo']['totalResults']))

c = 0
for i in js['items']:
    print(' > Video {}: {}'.format(c + 1, i['snippet']['title']))
    c += 1
