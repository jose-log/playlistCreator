
import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# This file is downloaded from the Youtube API Dashboard, once the application
# is registered and activated
CLIENT_SECRETS_FILE = 'youtube_secrets.json'

# Scopse are the type of permissions that the application needs to access user
# data while interacting with the API
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# API-specific macros
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def __get_authentincated_service():    

    print('  - Building the authenticated service...')

    # Get OAuth credentials
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

    #*******************************************
    # Request structure
    #*******************************************
    collection = service.videos()           # Extract collection of videos
    request = collection.list(**kwargs)     # HTTP Request object        
    
    return request.execute()

def request_liked_playlist():

    service = __get_authentincated_service()

    nxtPage = None
    i = 0
    files = []

    while True:
        
        try:
            print('  - Requesting query No {} to API'.format(i + 1))
            response = __request_service(
                service, 
                part = 'id,snippet,contentDetails',
                myRating = 'like',
                maxResults = 50,
                pageToken = nxtPage,
                fields = 'items(id,snippet(title),contentDetails(duration)),pageInfo,nextPageToken'
                )

        except:
            print('ERROR Requesting the API.')
            quit()

        if i is 0:
            total = response['pageInfo']['totalResults']
            inPage = response['pageInfo']['resultsPerPage']
        
        # save response to files
        outfile = 'videos_dump' + str(i+1) + '.json'
        fh = open(outfile, 'w')
        json.dump(response, fh, sort_keys=True, indent=4)
        fh.close()
        files.append(outfile)
        i += 1

        # index file
        ih = open('videos_index.txt', 'a')
        ih.write(outfile + '\n')
        ih.close()

        nxtPage = response.get('nextPageToken', None)
        if nxtPage is None:
            print('  - Total No of results: {}'.format(total))
            if total > inPage:
                if (total % inPage) > 0:
                    print('  - No of request iterations: {}'.format(int(total/inPage) + 1))
                else:
                    print('  - No of request iterations: {}'.format(int(total/inPage)))
            else:
                print('  - No of request iterations: 1')
            break 

    return files