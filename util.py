
import os
import re	# regular expressions
import json
from database import db

def request_youtube_files():

	files = []
	path = None

	while True:
		x = input('Enter the index file name: ')
		if len(x) is 0:
			#print('No files added.')
			path = 'videos_index.txt'
			break
		elif os.path.exists(x) is False:
			print('ERROR. File does NOT exists. Please try again')
		else:
			path = x
			break

	fh = open(path)
	print('  - Files Added:')
	for line in fh:
		files.append(line.strip())
		print('    > ' + line.strip())

	return files

def store_in_database(files):

	# Database
	likesDB = db('music.sqlite')

	n = 0
	# Extract info from files
	for f in files:
		fh = open(f)
		js = json.load(fh)
		print('\n' + f + ': {} items\n'.format(len(js['items'])))
		n += len(js['items'])

		videos = []
		item = {}
		c = 1
		for i in js['items']:
			item['title'] = i['snippet']['title']
			item['duration'] = __get_time(i['contentDetails']['duration'])
			item['youtubeID'] = i['id']
			videos.append(item.copy())
			print(' > Video {}: {} | id = {}'.format(c, i['snippet']['title'], i['id']))
			c += 1

		likesDB.insert_multiple_videos(videos)

	print('\n >> TOTAL ITEMS: ' + str(n))

	return likesDB

def __get_time(time):
	# ISO8601 Time format conversion

	RE_SEC = r'^P.*[TM](\d+)S$'
	RE_MIN = r'^P.*[TH](\d+)M.*S$'
	RE_H = r'^P.*[T](\d+)H.*M.*S$'
	RE_DAY = r'^P(\d+)DT.*H.*M.*S$'

	seconds = re.search(RE_SEC, time)
	minutes = re.search(RE_MIN, time)
	hours = re.search(RE_H, time)
	days = re.search(RE_DAY, time)

	s = 0
	if seconds is not None: s += int(seconds[1])
	if minutes is not None: s += int(minutes[1]) * 60
	if hours is not None: s += int(hours[1]) * 3600
	if days is not None: s += int(days[1]) * 86400

	return s