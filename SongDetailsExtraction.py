import requests
import pandas as pd

from DataExtraction import SpotifyAPI


class SpotifySongs(SpotifyAPI):

    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)

    def get_song_details(self):
        df = pd.read_csv("ExtractedSongInformation\\SongsInformation.csv")
        df1 = pd.DataFrame(data=None, columns=["Index", "SongID", "Danceability",
                                               "Energy", "Key", "Loudness", "Mode",
                                               "Speechiness", "Acousticness", "Instrumentalness",
                                               "Liveness", "Valence", "Tempo", "Duration_ms"])
        artist_name_list = df["ArtistName"]
        song_name_list = df["SongName"]
        song_id_list = df["SongID"]
        for index in range(0, len(artist_name_list)):
            authentication = self.perform_auth()
            if authentication:
                headers = {
                    "Authorization": f"Bearer {self.access_token}"
                }
            lookup_url = "https://api.spotify.com/v1/audio-features/" + f"{song_id_list[index]}"
            req = requests.get(url=lookup_url, headers=headers)
            if req.status_code not in range(200, 299):
                print("Not a valid request")
            data = req.json()
            print(f"Song: {song_name_list[index]}, Index: {index}, Query: {lookup_url}")
            query_data = {
                "Index": index,
                "SongID": song_id_list[index],
                "Danceability": data["danceability"],
                "Energy": data["energy"],
                "Key": data["key"],
                "Loudness": data["loudness"],
                "Mode": data["mode"],
                "Speechiness": data["speechiness"],
                "Acousticness": data["acousticness"],
                "Instrumentalness": data["instrumentalness"],
                "Liveness": data["liveness"],
                "Valence": data["valence"],
                "Tempo": data["tempo"],
                "Duration_ms": data["duration_ms"]
            }
            df1 = df1.append(query_data, ignore_index=True)
        return df1


if __name__ == "__main__":
    client_id = ""
    client_secret = ""
    spotify = SpotifySongs(client_id, client_secret)
    print(spotify.client_id, spotify.client_secret)
    df1 = spotify.get_song_details()
    df1.to_csv("ExtractedSongInformation\\SongFeatures.csv", index=False)
