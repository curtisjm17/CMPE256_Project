#!/bin/python

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle
import time
import random
import string
from datetime import datetime as dt
import pandas as pd

# Million Playlist Dataset contains playlists created between January 2010 and November 2017
class EasySpotipy():
    __ID     = 'fb03f1c6af28420db3441d201a8dea16'
    __SECRET = '543f352d8d694958abfcfde732a474ac'

    def __init__(self, id=__ID, secret=__SECRET, max_retries=10):
        creds    = SpotifyClientCredentials(client_id=id, client_secret=secret)
        self.sp_ = spotipy.Spotify(client_credentials_manager=creds, retries=max_retries)

    def getSP(self):
        return self.sp_

    # Super rudimentary but adds a level of needed randomness to the query
    def __generateRandomQueryAndOffset(self):
        query = random.choice(string.ascii_letters).lower()
        random_wildcard = random.randrange(3)
        if(random_wildcard == 0):
            query = query + '%'
        elif(random_wildcard == 1):
            query = '%' + query
        else:
            query = '%' + query + '%'
        offset = random.randrange(20)
        return [query, offset]

    '''
    Return a list of track IDs from a pseudo-random playlist
    '''
    def getRandomPlaylist(self, min_tracks=5, market='US'):
        latest_release_date = '2017-12-00'
        tracklist = []

        while len(tracklist) < min_tracks:
            # The API returns consistent results based on the query, so randomize it
            query_offset=self.__generateRandomQueryAndOffset()

            # query = f'{query_offset[0]}+market:{market}'
            # TODO - name query and market syntax doesn't work??
            playlists = self.sp_.search(q=query_offset[0], type='playlist', offset=query_offset[1])['playlists']

            while len(tracklist) < min_tracks and playlists['next']:
                playlists = self.sp_.next(playlists)['playlists']
                for playlist in playlists['items']:
                    # print(f"Processing the playlist {playlist['name']}")
                    results = self.sp_.playlist_items(playlist['id'])

                    # Drop playlists that don't meet the minimum number of tracks
                    if results['total'] < min_tracks:
                        continue

                    # The Million Playlist dataset includes playlists created between 1/2010 and 11/2017,
                    # so drop songs that were created after to help reduce some noise.
                    items = results['items']
                    for song in results['items']:
                        release_date = song['track']['album'].get('release_date')

                        if release_date and release_date > latest_release_date:
                            tracklist.append(song['track']['id'])
                    if len(tracklist) < min_tracks:
                        # After filtering out new songs, we don't meet min tracks, drop playlist
                        tracklist.clear()
                    else:
                        break
        return tracklist

    def getRandomPlaylistIndices(self, min_tracks=5, market='US'):
        playlist = self.getRandomPlaylist(min_tracks=min_tracks, market=market)

    def getRecommendations(self, seed_artists):
        if len(seed_artists > 5):
            return []


    def isGenre(self, track, genre):
        return False

    def EvaluateGenres(self, playlist, genre):
        return 0

    def PerformEvaluationMetrics(self, provided_playlists, recommended_playlists, num_trimmed, num_produced):
        '''
        '''
        return 0

def main():
    sp_api = EasySpotipy()

    random_playlist = sp_api.getRandomPlaylistIndices(min_tracks=10)
    print('Done!')

if __name__ == "__main__":
    main()
