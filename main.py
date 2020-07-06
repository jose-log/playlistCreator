#!/usr/bin/env python3

import spotify
import youtube
import database

YOUTUBE_DOWNLOAD 	= 1
STORE_DATABASE 		= 2
FILTER_TRACKS 		= 3
REQUEST_AUTH 		= 4
SEARCH_CATALOG 		= 5
APPEND_TRACKS 		= 6

def ask_user(question):
	
	ans = None
	while True:
		if (question == YOUTUBE_DOWNLOAD):
			x = input('Do you want to download \'Liked\' videos playlist? (Y/n) ')
		elif (question == STORE_DATABASE):
			x = input('Do you want to store videos info in database? (Y/n) ')
		elif (question == FILTER_TRACKS):
			x = input('Do you want to filter videos and extract tracks? (Y/n) ')
		elif (question == REQUEST_AUTH):
			x = input('Do you want to request new Spotify OAuth authorization? (Y/n) ')
		elif (question == SEARCH_CATALOG):
			x = input('Do you want to search in the spotify catalog? (Y/n) ')
		elif (question == APPEND_TRACKS):
			x = input('Do you want to append tracks to spotify playlist? (Y/n) ')

		if x in 'yY' or x is '':
			ans = True
			break
		elif x in 'nN':
			ans = False
			break
		elif x in 'qQ':
			exit()
		else:
			print('INVALID!')
	
	return  ans

###############################################################################
# 	MAIN PROGRAM
###############################################################################

if __name__ == '__main__':
#
# A series of steps must be followed to synchronize the Youtube Videos with the
# Spotify playlist. This script exectutes those steps as described below.
#
# Execution switches are implemented in the form of command line queries for
# the user to execute only the portion that's needed. This is to make the 
# script flexible and help with debugging.
#
# STEP 1: Request user to download liked videos playlist from Youtube.
# STEP 2: Create database and store results
# STEP 3: Filter videos to extract only songs
# STEP 4: Search in spotify library for song from youtube
# STEP 5: Insert all songs found in spotify into a new playlist

	print('\n\rHello World!\n\r')

	#**************************************************************************
	# STEP 1:
	# > Switch True:
	# Opens up a browser instance for user login and authorization, connects to
	# the YouTube Data API and requests the desired playlist. The response is 
	# stored in json-formatted files, together with an "index" file.
	# > Switch False
	# Command line requests for the "index" file that contains the 
	# json-formatted response previously saved
	#
	if ask_user(YOUTUBE_DOWNLOAD):
		pl_files = youtube.request_liked_playlist()
	else:
		pl_files = youtube.request_youtube_files()

	#**************************************************************************
	# STEP 2:
	# > Switch True:
	# Save all youtube results in a database using SQLite. Database details are 
	# shown in database.py
	# > Switch False:
	# Skip step. It is assumed that database has already been filled. Database
	# object is still created and initialized
	#
	db = database.db('music.sqlite')
	if (ask_user(STORE_DATABASE)):
		new_videos = database.store_in_database(pl_files, db)

	#**************************************************************************
	# STEP 3:
	# > Switch True:
	# Download video Info using YoutubeDL, and filter for songs only. Song 
	# names and artist are stored in database.
	# > Switch False:
	# Skip step. It is assumed that songs info is already in database
	#
	if (ask_user(FILTER_TRACKS)):
		new_tracks = db.filter_tracks(new_videos)
	
	#**************************************************************************
	# STEP 4:
	# Estabish connection to Spotify
	# > Switch True:
	# Search in spotify library for all the songs found from youtube playlist
	# and sync in database the spotify results (track uri)
	# > Switch False:
	# Skip step. It is assumed that spotify search results are already in 
	# database
	#
	spotify.get_authorization()
	if (ask_user(SEARCH_CATALOG)):
		db.search_spotify_catalog(new_tracks)

	#**************************************************************************
	# STEP 5:
	# Create new playlist to insert all searched items
	# > Switch True:
	# All the songs that have a valid spotify search result are added to the
	# playlist.
	# > Switch False:
	# Skip step. Nothing else is done
	#
	pl_id = spotify.create_spotify_playlist('Youtube Liked Vids')
	if (ask_user(APPEND_TRACKS)):
		db.append_tracks_to_playlist(pl_id, new_tracks)
	
	print('\n\n... FINISH! ...')