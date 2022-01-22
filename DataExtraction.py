import base64
import datetime
from urllib.parse import urlencode

import pandas as pd
import requests


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base 64 encoded string
        """
        if self.client_secret is None or self.client_id is None:
            raise Exception("Client id or Client secret cannot be null")
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(url=token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    @staticmethod
    def search_query():
        df = pd.read_json("Spotify\\StreamingHistory.json")
        songs_details = pd.DataFrame(data=None, columns=["Index", "SongName", "ArtistName", "SongID", "Popularity"])
        artist_name_list = df["artistName"]
        song_name_list = df["trackName"]
        for index in range(0, len(artist_name_list)):
            song_name = song_name_list[index]
            artist_name = artist_name_list[index]
            spotify.perform_auth()
            endpoint = "https://api.spotify.com/v1/search"
            headers = {"Authorization": f"Bearer {spotify.access_token}"}
            data = urlencode({
                "q": song_name,
                "artist": artist_name,
                "type": "track",
                "limit": 10,
                "market": "IN"
            })
            lookup_url = f"{endpoint}?{data}"
            req = requests.get(url=lookup_url, headers=headers)
            if req.status_code not in range(200, 299):
                print("Not a valid request")
            data = req.json()
            print("Index:", index)
            for items in data["tracks"]["items"]:
                if items["name"] == song_name and items["artists"][0]["name"] == artist_name:
                    print(f'Song Name: {items["name"]} ---- Artists Name: {items["artists"][0]["name"]}')
                    data = {"Index": index,
                            "SongName": items["name"],
                            "ArtistName": items["artists"][0]["name"],
                            "SongID": items["id"],
                            "Popularity": items["popularity"]}
                    songs_details = songs_details.append(data, ignore_index=True)
                    break
        return songs_details


if __name__ == "__main__":
    client_id = ""
    client_secret = ""
    spotify = SpotifyAPI(client_id, client_secret)
    songs_df = spotify.search_query()
    songs_df.to_csv("ExtractedSongInformation\\SongsInformation.csv", index=False)
