# CMPE256_Project
Download and extract the Million Playlist data set to the ./data folder (https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge#challenge-dataset)

To run the scripts to generate the Item-Item Recommender System, first execute the Process_Spotify_Data.ipynb file. This will generate a series of CSV files in the ./data folder that contains all the Spotify dataset. Next navigate to the ./Item_Item_Recommender folder. From there run the following scripts sequentially: Item_Item_Recommendation_MinHash_Playlist_Tracks.ipynb, Item_Item_Recommendation_LSH_Candidate_Pairs_Playlist_Tracks.ipynb, and Item_Item_Recommendation_Playlist_Testing.ipynb. It should noted that these scripts have significant run time, memory consumption, and disk space.
