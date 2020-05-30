#!/usr/bin/env python3

import sqlite3
import youtube_dl

# Table structure:
# 1. The whole title text of the video
#		- id	
#		- title
#		- length
#		- youtubeID
#		- id_track
# 2. Track names
#		- id
#		- name
#		- spotifyID
#		- id_artist
# 3. Artists
#		- id
#		- name
#		- spotifyID

class db(object):
	
	def __init__(self, name):
		self.name = name
		
		conn = sqlite3.connect(self.name)		# Connect to the database. If non-existent, create it.
		cur = conn.cursor()					# database handler object
		print('Database file \"' + self.name + '\" created')

		# Video Names table
		x = cur.execute('''
			CREATE TABLE IF NOT EXISTS videos (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
				title TEXT UNIQUE,
				length INTEGER,
				youtubeID TEXT UNIQUE,
				id_tracks INTEGER	)''')
		print('> Table VIDEOS created')

		# Tracks table
		cur.execute('''
			CREATE TABLE IF NOT EXISTS tracks (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
				name TEXT UNIQUE,
				spotifyID TEXT UNIQUE,
				id_artists INTEGER	)''')
		print('> Table TRACKS created')

		# Artists table
		cur.execute('''
		    CREATE TABLE IF NOT EXISTS artists (
		    	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		    	name TEXT UNIQUE,
		    	spotifyID TEXT UNIQUE	)''')
		print('> Table ARTISTS created')

		conn.commit()	# Save changes
		conn.close()	# Close database

	def insert_single_video(self, title, duration, youtubeID):

		conn = sqlite3.connect(self.name)		# Connect to the database. 
		cur = conn.cursor()						# database handler object

		cur.execute('INSERT OR IGNORE INTO videos (title, length, youtubeID) VALUES (?, ?, ?)',(title, duration, youtubeID))

		conn.commit()	# Save changes
		conn.close()	# Close database

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

	def filter_tracks(self):

		conn = sqlite3.connect(self.name)		# Connect to the database. 
		cur = conn.cursor()						# database handler object

		cur.execute('SELECT youtubeID FROM videos')
		items = cur.fetchall()

		tracks_info = {}

		for i in items:
			youtube_url = 'https://www.youtube.com/watch?v={}'.format(i[0])
			
			try:
				# use youtube_dl to collect the song name & artist name
				info = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
			except:
				print('ERROR: Video not available:', i)
				info['track'] = None
				info['artist'] = None

			track_name = info['track']
			artist_name = info['artist']

			# save all important info and skip any missing song and artist
			if track_name is not None and artist_name is not None:
				print(' > found: Artist: ' + artist_name + ', Song: ' + track_name)
				try:
					cur.execute('INSERT OR IGNORE INTO artists (name) VALUES (?)', (artist_name,))
					cur.execute('SELECT id FROM artists WHERE name = ?', (artist_name,))
					artist_id = cur.fetchone()
					cur.execute('INSERT OR IGNORE INTO tracks (name, id_artists) VALUES (?, ?)', (track_name, artist_id[0]))
					cur.execute('SELECT id FROM tracks WHERE name = ?', (track_name,))
					track_id = cur.fetchone()
					cur.execute('UPDATE videos SET id_tracks = ? WHERE youtubeID = ?', (track_id[0], i[0]))
					print("   added successfully")
				except:
					print("ERROR adding to database")