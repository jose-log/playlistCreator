# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import json

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
CLIENT_SECRETS_FILE = 'oauth.json'

def get_authentincated_service():    

    #*******************************************
    # Get credentials and create an API client
    #*******************************************
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(
    	host = 'localhost',
    	port = 8080, 
	    authorization_prompt_message = 'Please visit this URL: \n\r{url}', 
	    success_message = 'The auth flow is complete; you may close this window.',
	    open_browser = True)

    # Build the Service object:
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def request_service(service, **kwargs):

    #*******************************************
    # Request structure
    #*******************************************
    collection = service.videos()           # Extract collection of videos
    request = collection.list(**kwargs)     # HTTP Request object        
    return request.execute()                # Execute the request and get a response

if __name__ == "__main__":

    print('\n\rHello World!\n\r< YOUTUBE INFO DOWNLOADER >')

    x_yes = 'yY'
    x_no = 'nN'
    x_quit = 'qQ'
    download = None
    files = []

    while download is None:
        x = input('Do you want to download \'Liked\' videos playlist? (Y/n)')
        if x in x_yes or x is '':
            download = True
            break
        elif x in x_no:
            download = False
            break
        elif x in x_quit:
            exit()
        else:
            print('INVALID!')
    
    if download is True:

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        print('Building the authenticated service...')
        service = get_authentincated_service()

        nxtPage = None
        i = 0
        while True:
            
            try:
                print('Requesting query No {} to API'.format(i + 1))
                response = request_service(service, 
                                            part = 'snippet,contentDetails',
                                            myRating = 'like',
                                            maxResults = 50,
                                            pageToken = nxtPage)
            except:
                print('ERROR Requesting the API. Exiting.')
                print(response)
                quit()

            if i is 0:
                total = response['pageInfo']['totalResults']
                inPage = response['pageInfo']['resultsPerPage']
            
            # save response to file
            outfile = 'videos_dump' + str(i+1) + '.json'
            fh = open(outfile, 'w')
            json.dump(response, fh, sort_keys=True, indent=4)
            fh.close()
            files.append(outfile)
            i += 1

            nxtPage = response.get('nextPageToken', None)
            if nxtPage is None:
                print('Total No of results: {}'.format(total))
                if total > inPage:
                    if (total % inPage) > 0:
                        print('No of request iterations: {}'.format(int(total/inPage) + 1))
                    else:
                        print('No of request iterations: {}'.format(int(total/inPage)))
                else:
                    print('No of request iterations: 1')
                break 

    else:

        print('Enter the file names to be evaluated. Enter \'q\' when finished')
        i = 1
        x_quit = 'qQ'
        while True:

            x = input('File {}: '.format(i))
            if x is '' or x in x_quit:
                if len(files) is 0:
                    print('No files added.')
                else:
                    break
            elif x is ' ':
                files.append('videos_dump.json')
                break
            elif os.path.exists(x):
                files.append(x)
                i += 1
            else:
                print('ERROR. File does NOT exists. Please try again')

    # Extract info from files
        
    for f in files:
        fh = open(f)
        js = json.load(fh)
        if files.index(f) is 0:
            print(' > Total Results: {}\n'.format(js['pageInfo']['totalResults']))
        print('\n\n' + f + ':\n\n')
        print(' > Results in file: {}'.format(js['pageInfo']['resultsPerPage']))

        # Retrieving Useful Info
        c = 0
        for i in js['items']:
            print(' > Video {}: {} | time = {}'.format(c + 1, i['snippet']['title'], i['contentDetails']['duration']))
            c += 1
    
    print('\n\n... FINISH! ...')
