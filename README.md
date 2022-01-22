# Spotify Data Analysis
 
Analysis of Spotify streaming history with python.

### DataExtraction.py
    This python script uses StreamingHistory.json file which contains a list of items (e.g. songs, videos, and podcasts) 
    listened to or watched in the past year, including:
        1. Date and time of when the stream ended in UTC format (Coordinated Universal Time zone).
        2. Name of "creator" for each stream (e.g. the artist name if a music track).
        3. Name of items listened to or watched (e.g. title of music track or name of video).
        4. “msPlayed”- Stands for how many mili-seconds the track was listened to.

    From this file we use the name of the song along with the name of the artist of the song to get the track id.
    By passing the name of the song and the artist to spotify's web API search function we get a json file containing
    all the possible results of the song. From the json file we select the first entry we find which matches the song
    as well as the artist name. From that entry, we store the track id and the popularity.

### MergeSongsWithId.ipynb
    To merge the extracted song id with the orignal dataframe

### SongDetailsExtraction.py
    This python script uses the file "SongInfoWithId.csv" to get the features of a song such as danceability, energy, 
    key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence and tempo.
    These features are then stored in a dataframe and exported as a csv file.

### MergeSongsFeatures.ipynb
    This python notebook is used to merge dataframe containing the song_id and the dataframe containing the song features
    i.e SongInfoWithId.csv and SongFeatures.csv

### ExploratoryDataAnalysis.ipynb
    Python notebook which analysis the song data in the csv file "SpotifySongs.csv".
    