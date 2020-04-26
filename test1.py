#!/usr/bin/env python3

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
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
    # Clarification: https://github.com/singingwolfboy/flask-dance/issues/129
    # Flask-Dance is built on top of oauthlib, a Python toolkit that implements 
    # the OAuth specifications. The specification for OAuth 2 requires that all 
    # communication must occur over secure HTTPS -- if any communication occurs 
    # over insecure HTTP, it's vulnerable to attack. As a result, oauthlib raises 
    # an error if you use insecure HTTP. However, most people don't want to spend 
    # the time and effort to configure secure HTTPS for doing local testing -- it's 
    # only a problem for production, not for development.
    # As a result, oauthlib allows you to disable this check. If you set the 
    # OAUTHLIB_INSECURE_TRANSPORT environment variable, it will not check for secure
    # HTTPS, and allow the OAuth dance to continue whether or not it is secure. 
    # Disabling this check is intended only for development, not for production -- 
    # in production, you must configure secure HTTPS to make sure communication happen 
    # securely.

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "oauth.json"

    #*******************************************
    # Get credentials and create an API client
    #*******************************************
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server(
    	host='localhost',
    	port=8080, 
	    authorization_prompt_message='Please visit this URL: {url}', 
	    success_message='The auth flow is complete; you may close this window.',
	    open_browser=True)
    # Build the Service object:
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    #*******************************************
    # Request structure
    #*******************************************
    # channels():   function for the Channels collection
    collection = youtube.channels()
    # list():       method of the given collection
    request = collection.list(  part="id,status,contentDetails",
                                id="UCR9ay2jZLzQLw_E743NO-tQ")    # HTTP Request object        
    # Execute the request and get a response
    response = request.execute()

    # Dump JSON response to screen
    print(json.dumps(response, sort_keys=True, indent=4))
    print('\n\n\n\n\n***********************************')
    print('flow:')
    print(flow)
    print('credentials:')
    print(credentials)
    print('youtube:')
    print(youtube)
    print('collection:')
    print(collection)
    print('request:')
    print(request)
    print('response:')
    print(response)

if __name__ == "__main__":
    main()

'''
HTTP Requests: http://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.http.HttpRequest-class.html

Accessing the JSON data:
print('Num 5 cent stamps: %d'.format(response['count']))
print('First stamp name: %s'.format(response['items'][0]['name']))
'''
