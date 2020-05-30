#!/usr/bin/env python3

import spotify
import youtubeDL
import youtube
import util

def ask_for_playlist_download():
	# User is asked whether to download all the Liked Videos list from Youtube
	download = None
	while True:
	    x = input('Do you want to download \'Liked\' videos playlist? (Y/n) ')
	    if x in 'yY' or x is '':
	        download = True
	        break
	    elif x in 'nN':
	        download = False
	        break
	    elif x in 'qQ':
	        exit()
	    else:
	        print('INVALID!')
	
	return  download

###############################################################################
# 	MAIN PROGRAM
###############################################################################

if __name__ == '__main__':

	print('\n\rHello World!\n\r')

	if ask_for_playlist_download():
		# Connects to the YouTube Data API and requests the desired playlist.
		pl_files = youtube.request_liked_playlist()
	    
	else:
		# If files are already downloaded, it requests the file names
		pl_files = util.request_youtube_files()

	# Save all results in a database using SQLite
	db = util.store_in_database(pl_files)

	db.filter_tracks()



	
	print('\n\n... FINISH! ...')