#!/bin/python

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pickle
import time
import random
import string
from datetime import datetime as dt
import pandas as pd
import numpy as np

# Million Playlist Dataset contains playlists created between January 2010 and November 2017
class EasySpotipy():
    __TRACK_ID_MAP = 'data/tracks.csv'

    def __init__(self, username=None, track_id_map=__TRACK_ID_MAP, max_retries=10, cred_file='data/spotipy.txt'):
        with open(cred_file) as f:
            id = f.readline()[:-1]
            secret = f.readline()

        token  = spotipy.util.prompt_for_user_token(
                 username=username,
                 scope='playlist-modify-public',
                 client_id=id,
                 client_secret=secret,
                 redirect_uri="http://localhost:8888")
        self.sp_ = spotipy.Spotify(auth=token)

        # Track ID Map
        self.track_id_map_ = pd.read_csv(track_id_map, header=None, names=['track_index', 'track_id'])
        self.username = username

    def getSP(self):
        return self.sp_

    def getNameAndArtistFromTrack(self, track):
        name = track['name']
        artists = ''
        for i, artist in enumerate(track['artists']):
            if i != 0:
                artists += ', '
            artists += artist['name']
        return name + ' - ' + artists

    def getTrackIDFromIndex(self, index):
        track_id = self.track_id_map_[self.track_id_map_.track_index == index].track_id
        if not track_id.empty:
            return track_id.values[0]
        else:
            return -1

    def getNameAndArtistFromTrackID(self, ID):
        track = self.sp_.track(ID)
        return self.getNameAndArtistFromTrack(track)

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
    Return a np array of tracks from a pseudo-random playlist.
    NP Array format:
    [[track ID, index in map, name - artist(s)],
     [    ID-2,      index-2,           name-2],
     [    ID-3,      index-3,           name-3],
                        ...
     [    ID-N,      index-N,           name-N]]
    Will only return tracks that are contained in the track ID map
    '''
    def getRandomPlaylist(self, min_tracks=5, max_tracks=200, market='US'):
        latest_release_date = '2017-12-00'
        tracklist = []

        while len(tracklist) < min_tracks:
            # The API returns consistent results based on the query, so randomize it
            query_offset=self.__generateRandomQueryAndOffset()
            try:
                playlists = self.sp_.search(q=query_offset[0], type='playlist', market=market, offset=query_offset[1])['playlists']
            except:
                # Shhhh HTTP error error, try again!
                time.sleep(1)
                continue

            while len(tracklist) < min_tracks and playlists['next']:
                try:
                    playlists = self.sp_.next(playlists)['playlists']
                except:
                    # Shhhh HTTP error, try again!
                    time.sleep(1)
                    continue
                for playlist in playlists['items']:
                    # print(f"Processing the playlist {playlist['name']}")
                    results = self.sp_.playlist_items(playlist['id'])

                    # Drop playlists that don't meet the minimum number of tracks
                    if results['total'] < min_tracks:
                        continue

                    # The 8 Million Playlist dataset includes playlists created between 1/2010 and 11/2017,
                    # so drop songs that were created after to help reduce some noise.
                    items = results['items']
                    for song in results['items']:
                        if not song['track']:
                            continue
                        try:
                            release_date = song['track']['album'].get('release_date')
                        except:
                            continue

                        if release_date and release_date < latest_release_date:
                            track_id = song['track']['id']
                            name_and_artist = self.getNameAndArtistFromTrack(song['track'])
                            index = self.track_id_map_[self.track_id_map_.track_id == track_id].track_index
                            if not index.empty: # If the ID was found
                                entry = np.array([track_id, index.values[0], name_and_artist], dtype=object)
                                tracklist.append(entry)
                        if len(tracklist) >= max_tracks:
                            break
                    if len(tracklist) < min_tracks:
                        # After filtering out new songs, if we don't meet min tracks, drop playlist
                        tracklist.clear()
                    else:
                        break
        return np.array(tracklist)

    def createNewPlaylist(self, tracks, playlist_name, user='Hochstadt'):
        playlist_id = self.sp_.user_playlist_create(user, playlist_name)
        self.sp_.playlist_add_items(playlist_id['id'], tracks)
        return playlist_id

def main():
    sp_api = EasySpotipy(username='Hochstadt')

    # sp_api.getSP().
    # SP = sp_api.getSP()
    # print(SP.me())
    # ID     = '8ec413d8eed346bd9f88fab92cee1dfd'
    # SECRET = '1bc60fc14b0347fa971eee940e7ecd24'
    # creds  = SpotifyClientCredentials(client_id=ID, client_secret=SECRET)
    # oauth  = SpotifyOAuth(client_id=ID, client_secret=SECRET, redirect_uri='localhost:8080')
    # sp     = spotipy.Spotify(client_credentials_manager=creds, auth_manager=oauth)


    # playlist_ID = sp.user_playlist_create('Hochstadt', 'Potato Salad')



    # Get random playlist
    # Put into playlist
    # insert into LSH model
    # Add new playlist

if __name__ == "__main__":
    main()
