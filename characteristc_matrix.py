#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Pyspark not needed for this script, jsut testing

#import pyspark
#from pyspark.sql import SparkSession


# In[7]:


import sys
import json
import time
import os


# In[217]:


import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix
from scipy.sparse import hstack
from scipy.sparse import vstack
import scipy.sparse


# In[195]:


data_location = "/media/sf_vm_dropbox/data/spotify_data/data"
NUM_PLAYLISTS = 1000000
NUM_ARTISTS = 295860 #<- from stats.txt


# In[ ]:


#Helpful commands:
#type() tells type
#sys.getsizeof(obj) tell size in bytes of obj


# In[13]:


def process_playlists(path):
    filenames = os.listdir(path)
    for filename in sorted(filenames):
        if filename.startswith("mpd.slice.") and filename.endswith(".json"):
            fullpath = os.sep.join((path, filename))
            f = open(fullpath)
            js = f.read()
            f.close()
            mpd_slice = json.loads(js)
            for playlist in mpd_slice["playlists"]:
                print_playlist(playlist)
def print_playlist(playlist):
    print("=====", playlist["pid"], "====")
    print("name:          ", playlist["name"])
    ts = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(playlist["modified_at"])
    )

    print("last_modified: ", ts)
    print("num edits: ", playlist["num_edits"])
    print("num followers: ", playlist["num_followers"])
    print("num artists: ", playlist["num_artists"])
    print("num albums: ", playlist["num_albums"])
    print("num tracks: ", playlist["num_tracks"])
    print()
    for i, track in enumerate(playlist["tracks"]):
        print(
            "   %3d %s - %s - %s"
            % (i + 1, track["track_name"], track["album_name"], track["artist_name"])
        )
    print()


# In[231]:


test_index = 1
filenames = os.listdir(data_location)
#filenames = filenames[0:test_index+1]
playlist_index = 0
artist_dict = dict()
artist_id_array = []
total_artist_count = 0
charmat = csc_matrix((NUM_ARTISTS,1000))
file_index = 0
for filename in sorted(filenames):
    if filename.startswith("mpd.slice.") and filename.endswith(".json"):
        f = open(fullpath)
        js = f.read()
        f.close()
        mpd_slice = json.loads(js)
        start_time = time.time()
        print('Filename: ', filename)
        charmat = csc_matrix((NUM_ARTISTS,1000))
        playlist_index = 0
        for playlist in mpd_slice["playlists"]:
            print('p',playlist_index, sep='', end=', ')
            #Per each track in given playlist:
            
            for track in playlist['tracks']:                
                artist_name = track['artist_name']
                #if arist is in charmat increment that location, 
                #else save off artist name to create new addition to 
                #charmat
                if artist_name in artist_dict:
                    #Already identified artist
                    artist_index = artist_dict[artist_name]
                    charmat[artist_index, playlist_index] = charmat[artist_index, playlist_index] + 1
                    
                else:
                    #Brand new artist:
                    #add to dictionary w/index
                    artist_dict[artist_name] = total_artist_count
                    #add to matrix
                    charmat[total_artist_count, playlist_index] = 1                    
                    #increment count
                    total_artist_count = total_artist_count + 1
                    if total_artist_count >= NUM_ARTISTS:
                        print('Total artist count is larger than spotify info. Will cause error')                
                

            #increment playlist id:
            playlist_index = playlist_index + 1
        print('Time elapsed for file', filename, '= ', time.time() - start_time)
        fname = os.sep.join(('formatted_data', 'charmat_pt_' + str(file_index)))
        scipy.sparse.save_npz(os.sep.join((data_location, fname)), charmat)
        file_index = file_index + 1
            

