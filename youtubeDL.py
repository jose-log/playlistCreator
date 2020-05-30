
import youtube_dl

import json
import os

###############################################################################
# 	MAIN PROGRAM
###############################################################################

if __name__ == '__main__':
    
	while True:
		filename = input('Enter the file name with JSON-formatted songs. Enter \'q\' when finished: ')
		if filename is None or filename in 'qQ':
			print('Quitting...')
			exit()
		elif os.path.exists(filename):
			break
		else:
			print('ERROR. File does NOT exists. Please try again')

	fh = open(filename)
	js = json.load(fh)
	fh.close()

	tracks_info = {}

	for i in js['items']:

		youtube_url = 'https://www.youtube.com/watch?v={}'.format(i['id'])
		# use youtube_dl to collect the song name & artist name
		try:
			info = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
		except:
			print('ERROR: Video not available:', i['snippet']['title'])
			info['track'] = None
			info['artist'] = None

		track_name = info['track']
		artist = info['artist']

		if track_name is not None and artist is not None:
			# save all important info and skip any missing song and artist
			video_title = i['snippet']['title']
			tracks_info[video_title] = {
				'youtube_url': youtube_url,
				'track_name': track_name,
				'artist': artist
			}

	print(tracks_info)

	print('\n\n... FINISH! ...')