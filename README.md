
# Syncing YouTube and Spotify with Python

Extracting _"liked"_ videos playlist from YouTube and syncing with Spotify.

A blog post describing the project: https://joselog.co/python/python_and_apis

I first watched this project here: https://www.youtube.com/watch?v=7J_qcttfnJA&list=WL&index=79&t=0s

The original project repo is: https://github.com/TheComeUpCode/SpotifyGeneratePlaylist

This is my own implementation of the original project. I took it as a learning resource for Python itself and web APIs (including OAuth2.0), besides many web applications concepts. Some additions and improvements to the original project:

* _Using SQLite Databases_
* _Spotify OAuth2.0 Authentication_
* _Improved YouTube Data API implementation_
* _Execution switches_
* _Support for subsequent script executions_
* _Error Handling_

## Program steps

The script is divided into five steps:

1. Request user to download “liked” videos playlist from Youtube.
1. Create database and store videos
1. Filter videos to extract only songs
1. Search songs in Spotify catalog
1. Append all songs into a new Spotify playlist

## Learning Resources:

* For Python, I went through all the [Python For Everybody](https://www.py4e.com/) series. It's free, it's all in YouTube, it makes part of a [Coursera specialization](https://www.coursera.org/specializations/python). 

* Here's the [Youtube Data API documentation](https://developers.google.com/youtube/v3/docs/playlists).

* Here's the [Spotify API documentation](https://developer.spotify.com/documentation/web-api/reference/playlists/)

* For OAuth2.0 Authentication with Spotify, I took the [Spotipy](https://spotipy.readthedocs.io/en/2.13.0/) Python module as a reference.

Finally, thanks to [The Come Up](https://www.youtube.com/channel/UC-bFgwL_kFKLZA60AiB-CCQ) channel. It was great to find this project.

---

## License

Released under the [MIT License](LICENSE) - 2020 Jose Logreira