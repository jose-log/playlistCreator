#!/usr/bin/env python3

import sqlite3

db_name = 'music.sqlite'
conn = 0
cur = 0

# Table structure:
# 1. The whole title text of the video
#		- id	
#		- video_title
#		- id_track
#		- id_artist
# 2. Track names
#		- id
#		- name
# 3. Artists
#		- id
#		- name

def db_init():
	
	conn = sqlite3.connect('music.sqlite')		# Connect to the database. If non-existent, create it.
	cur = conn.cursor()							# database handler object
	print('Database file \"' + db_name + '\" created')
	
	# Video Names table
	x = cur.execute('''
		CREATE TABLE IF NOT EXISTS videos (
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			title TEXT UNIQUE,
			length INTEGER,
			id_tracks INTEGER,
			id_artists INTEGER	)''')
	print('> Table VIDEOS created')

	# Tracks table
	cur.execute('''
		CREATE TABLE IF NOT EXISTS tracks (
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			name TEXT UNIQUE	)''')
	print('> Table TRACKS created')

	# Artists table
	cur.execute('''
	    CREATE TABLE IF NOT EXISTS artists (
	    	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	    	name TEXT UNIQUE	)''')
	print('> Table ARTISTS created')

	conn.commit()	# Save changes
	conn.close()	# Close database
	
	return 

def db_insert_video(title, duration):

	conn = sqlite3.connect('music.sqlite')		# Connect to the database. If non-existent, create it.
	cur = conn.cursor()							# database handler object

	cur.execute('INSERT INTO videos (title, length) VALUES (?, ?)',(title, duration))

	conn.commit()	# Save changes
	conn.close()	# Close database

