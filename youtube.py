#!/usr/bin/env python3

import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# This file is downloaded from the Youtube API Dashboard, once the application
# is registered and activated
CLIENT_SECRETS_FILE = 'secrets_youtube.json'

# Scopse are the type of permissions that the application needs to access user
# data while interacting with the API
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# API-specific macros
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Files' Names
INDEX_FILE = 'videos_index.txt'
VIDEOS_BASENAME = 'videos_dump'

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def __get_authentincated_service():    

    print('  - Building the authenticated service...')

    # Get OAuth credentials
    # Google OAuth entirely handled by the Google Python Client libraries
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    
    # Create local server to interact with OAuth server.
    # User is required to grant access to the application.
    credentials = flow.run_local_server(
    	host = 'localhost',
    	port = 8080, 
	    authorization_prompt_message = 'Please visit this URL: \n\r{url}', 
	    success_message = 'The auth flow is complete; you may close this window.',
	    open_browser = True)

    # Build the Service object:
    service = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    
    return service

def __request_service(service, **kwargs):

    collection = service.videos()           # Extract collection of videos
    request = collection.list(**kwargs)     # HTTP Request object        
    
    return request.execute()

def request_liked_playlist():

    service = __get_authentincated_service()

    # No of response results is limited!, thus, multiple queries must be 
    # performed in order to get the entire list of videos. Using page pointers
    # (available in the json response) the subsequent requests ask for the next
    # block of videos to be downloaded
    i = 1
    files = []
    nxtPage = None
    while True:
        
        try:
            print('  - Requesting query No {} to Youtube Data API'.format(i))
            response = __request_service(
                service, 
                part = 'id,snippet,contentDetails',
                myRating = 'like',
                maxResults = 50,
                pageToken = nxtPage,
                fields = 'items(id,snippet(title),contentDetails(duration)),pageInfo,nextPageToken'
                )

        except:
            print('ERROR Requesting Youtube Data API.')
            print(response)
            quit()
                       
        # save response to files
        outfile = VIDEOS_BASENAME + str(i) + '.json'
        fh = open(outfile, 'w')
        json.dump(response, fh, sort_keys=True, indent=4)
        fh.close()
        files.append(outfile)

        # index file
        fh = open(INDEX_FILE, 'a')
        fh.write(outfile + '\n')
        fh.close()

        nxtPage = response.get('nextPageToken', None)
        if nxtPage is None:
            try:
                total = response['pageInfo']['totalResults']
            except:
                print('ERROR. JSON response not properly formatted')
                quit()
            print('  > Total No of results: {}'.format(total))
            print('  > No of request iterations: {}'.format(i))
            break 
        
        i += 1

    return files

def request_youtube_files():

    files = []
    path = None

    while True:
        x = input('Enter the index file name: ')
        if len(x) is 0:
            path = 'videos_index.txt'
            if os.path.exists(path) is True:
                break
            else:
                print('WARNING: No files added. Try Again')
        elif os.path.exists(x) is False:
            print('ERROR. File does NOT exists. Please try again')
        else:
            path = x
            break

    fh = open(path)
    print('  - Files Added:')
    for line in fh:
        files.append(line.strip())
        print('  * ' + line.strip())

    return files