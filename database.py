#!/usr/bin/env python3

import sqlite3
import youtube_dl
import json
import re
import os
import spotify

#******************************************************************************
# Table structure:
# 1. The whole title text of the video
#		- id 		--> primary key
#		- title
#		- length
#		- youtubeID
#		- id_track 	--> foreing key
# 2. Track names
#		- id 		--> primary key
#		- name
#		- spotifyID
#		- id_artist --> foreing key
# 3. Artists
#		- id 		--> primary key
#		- name
#		- spotifyID
#
class db(object):

	name = None
	
	def __init__(self, name):
		self.name = name
		
		if os.path.exists(self.name) is True:
			print('  - Opening databajse file \"' + self.name + '\"')
		else:
			print('  - Creating database file \"' + self.name + '\"')
		conn = sqlite3.connect(self.name)	# Connect to the database. If non-existent, create it.
		cur = conn.cursor()					# database handler object

		# Video Names table
		x = cur.execute('''
			CREATE TABLE IF NOT EXISTS videos (
				id 			INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
				title 		TEXT UNIQUE,
				length 		INTEGER,
				youtubeID 	TEXT UNIQUE,
				id_tracks 	INTEGER	)''')

		# Tracks table
		cur.execute('''
			CREATE TABLE IF NOT EXISTS tracks (
				id 			INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
				name 		TEXT UNIQUE,
				spotifyID 	TEXT UNIQUE,
				id_artists 	INTEGER	)''')

		# Artists table
		cur.execute('''
		    CREATE TABLE IF NOT EXISTS artists (
		    	id 			INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		    	name 		TEXT UNIQUE,
		    	spotifyID 	TEXT UNIQUE	)''')
		
		conn.commit()	# Save changes
		conn.close()	# Close database

	#**************************************************************************
	def insert_single_video(self, title, duration, youtubeID):

		conn = sqlite3.connect(self.name)		# Connect to the database. 
		cur = conn.cursor()						# database handler object

		cur.execute('INSERT OR IGNORE INTO videos (title, length, youtubeID) VALUES (?, ?, ?)',(title, duration, youtubeID))

		conn.commit()	# Save changes
		conn.close()	# Close database

	#**************************************************************************
	def insert_multiple_videos(self, videos):

		conn = sqlite3.connect(self.name)		# Connect to the database. 
		cur = conn.cursor()						# database handler object

		for i in videos:
			cur.execute('''
				INSERT OR IGNORE INTO videos (title, length, youtubeID) 
				VALUES (?, ?, ?)''',(i['title'], i['duration'], i['youtubeID'])
				)

		conn.commit()	# Save changes
		conn.close()	# Close database

	#**************************************************************************
	def filter_tracks(self):

		print('  - Filtering Songs Using YoutubeDL')

		conn = sqlite3.connect(self.name)		# Connect to the database. 
		cur = conn.cursor()						# database handler object

		cur.execute('SELECT youtubeID FROM videos')
		items = cur.fetchall()

		for i in items:
			video_id = i[0]
			youtube_url = 'https://www.youtube.com/watch?v={}'.format(video_id)
			
			try:
				# use youtube_dl to collect the song name & artist name
				info = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
				track_name = info.get('track', None)
				artist_name = info.get('artist', None)
			except:
				print('WARNING: Video not available. Youtube ID:', video_id)
				track_name = None
				artist_name = None

			# save all important info and skip any missing song and artist
			if track_name is not None and artist_name is not None:
				print('  > found: Artist: ' + artist_name + ', Song: ' + track_name)
				try:
					cur.execute('INSERT OR IGNORE INTO artists (name) VALUES (?)', (artist_name,))
					cur.execute('SELECT id FROM artists WHERE name = ?', (artist_name,))
					artist_id = cur.fetchone()
					cur.execute('INSERT OR IGNORE INTO tracks (name, id_artists) VALUES (?, ?)', (track_name, artist_id[0]))
					cur.execute('SELECT id FROM tracks WHERE name = ?', (track_name,))
					track_id = cur.fetchone()
					cur.execute('UPDATE videos SET id_tracks = ? WHERE youtubeID = ?', (track_id[0], video_id))
				except:
					print('ERROR when adding to database: ' + track_name + ', ' + artist_name + 'NOT ADDED')

		conn.commit()	# Save changes
		conn.close()	# Close database

	#**************************************************************************
	def filter_single_track(self, youtubeID):

		conn = sqlite3.connect(self.name)		# Connect to the database. 
		cur = conn.cursor()						# database handler object

		cur.execute('SELECT youtubeID FROM videos WHERE youtubeID = ?', (youtubeID,))
		item = cur.fetchone()	# returns tuples
		item = item[0]
		youtube_url = 'https://www.youtube.com/watch?v={}'.format(item)

		try:
			# use youtube_dl to collect the song name & artist name
			info = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
			track_name = info['track']
			artist_name = info['artist']
		except:
			print('ERROR: Video not available. Youtube ID:', item)
			track_name = None
			artist_name = None

		if track_name is not None and artist_name is not None:
			if (isinstance(track_name, str)):
				print('  - Track Name:', track_name)
			else:
				print('  - WARNING: Track name not a string.')
				print(track_name)
			if (isinstance(artist_name, str)):
				print('  - Artist Name:', artist_name)
			else:
				print('  - WARNING: Artist name not a string.')
				print(artist_name)
		else:
			print('  - SORRY, no track & artist found')

		conn.commit()	# Save changes
		conn.close()	# Close database

	#**************************************************************************
	def search_spotify_catalog(self):

		conn = sqlite3.connect(self.name)		# Connect to the database. 
		cur = conn.cursor()						# database handler object

		cur.execute('SELECT tracks.id, tracks.name, artists.name FROM tracks JOIN artists ON tracks.id_artists = artists.id')
		items = cur.fetchall()

		print('\n  - Total # of Tracks: ' + str(len(items)))
		print('  - Searching in Spotify Catalog')
		for i in items:
			track_id = i[0]
			track_name = i[1]
			artist_name = i[2]
			print(' > Search: ' + track_name + ', ' + artist_name)
			uri = spotify.search_catalog(track_name, artist_name)
			if uri is not None:
				cur.execute('UPDATE tracks SET spotifyID = ? WHERE id = ?', (uri, track_id))
			else:
				print('WARNING: not found')

		conn.commit()	# Save changes
		conn.close()	# Close database

	#**************************************************************************
	def append_tracks_to_playlist(self, playlist_id):

		conn = sqlite3.connect(self.name)		# Connect to the database. 
		cur = conn.cursor()						# database handler object

		cur.execute('SELECT tracks.spotifyID FROM tracks WHERE spotifyID IS NOT NULL')
		items = cur.fetchall()

		conn.commit()	# Save changes
		conn.close()	# Close database

		tracks = []
		for i in items:
			tracks.append(i[0])

		spotify.insert_into_playlist(playlist_id, tracks)

#******************************************************************************
def store_in_database(files, db_obj):

	n = 0
	# Extract info from files
	for f in files:
		if os.path.exists(f):
			fh = open(f)
			js = json.load(fh)
			fh.close()
		else:
			print('ERROR. File ' + f + ' not found')
			exit()
		
		try:
			print('\n' + f + ': {} items\n'.format(len(js['items'])))
		except:
			print('ERROR. JSON file not properly formatted')
			exit()
		
		n += len(js['items'])
		videos = []
		item = {}
		c = 1
		try:
			for i in js['items']:
				item['title'] = i['snippet']['title']
				item['duration'] = __get_time(i['contentDetails']['duration'])
				item['youtubeID'] = i['id']
				videos.append(item.copy())
				print('  > Video {}: {} | id = {}'.format(c, i['snippet']['title'], i['id']))
				c += 1
		except:
			print('ERROR. JSON file not properly formatted')
			exit()

		db_obj.insert_multiple_videos(videos)

	print('\n >> TOTAL ITEMS: ' + str(n) + '\n')

#******************************************************************************
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