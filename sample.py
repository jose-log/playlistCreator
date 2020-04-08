# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "oauth_localhost.json"

    #*******************************************
    # Get credentials and create an API client
    #*******************************************
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    # Build the Service object:
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    #*******************************************
    # Request structure
    #*******************************************
    # channels():   function for the Channels collection
    collection = youtube.channels().list(part="id,status,contentDetails",id="UCR9ay2jZLzQLw_E743NO-tQ")    # HTTP Request object        
    # Execute the request and get a response
    response = request.execute()

    # Dump JSON response to screen
    print(json.dumps(response, sort_keys=True, indent=4))

    json_data = response.read().decode()
     #= json.loads(response)

    fh = open('dump.json', 'w')
    file.write(json_data)
    fh.close()

if __name__ == "__main__":
    main()


'''
HTTP Requests: http://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.http.HttpRequest-class.html
'''
