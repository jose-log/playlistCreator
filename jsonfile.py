# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import json

response = r'''{
    "etag": "\"xwzn9fn_LczrfK9QS3iZcGzqRGs/e88fQuiwm1pdBG9jfgnl39-7Wdw\"",
    "items": [
        {
            "contentDetails": {
                "relatedPlaylists": {
                    "favorites": "FLR9ay2jZLzQLw_E743NO-tQ",
                    "likes": "LLR9ay2jZLzQLw_E743NO-tQ",
                    "uploads": "UUR9ay2jZLzQLw_E743NO-tQ",
                    "watchHistory": "HL",
                    "watchLater": "WL"
                }
            },
            "etag": "\"xwzn9fn_LczrfK9QS3iZcGzqRGs/2UaeN5WJ7Oi7xK2t-n28s9F2WMA\"",
            "id": "UCR9ay2jZLzQLw_E743NO-tQ",
            "kind": "youtube#channel",
            "status": {
                "isLinked": true,
                "longUploadsStatus": "allowed",
                "privacyStatus": "public"
            }
        }
    ],
    "kind": "youtube#channelListResponse",
    "pageInfo": {
        "resultsPerPage": 1,
        "totalResults": 1
    }
}'''

data = '''{
        "name" : "Chuck",
        "phone" : {
                "type" : "intl",
                "number" : "+1 734 303 4456"
        },
        "email" : {
                "hide" : "yes"
        }
}'''


def main():

    js = json.loads(response)
    print(type(js))
    print(js)
    print('*******************************************')
    print('*******************************************')
    print(js.items())
    print('*******************************************')
    print('*******************************************')
    # Dump JSON response to screen
    print(json.dumps(js, sort_keys=True, indent=4))
    out = 'jsondump.json'
    with open(out, 'w') as outfile:
        json.dump(js, outfile, sort_keys=True, indent=4)

if __name__ == "__main__":
    main()
