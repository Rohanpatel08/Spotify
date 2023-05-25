"""
This module defines the Authorization logic for getting the token from spotify
"""
import json
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth


class Authorization:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_api = "https://accounts.spotify.com/api/token"
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.data = dict(grant_type="client_credentials")
        self.access_token = None
        self.token_type = None
        self.expires_in = 3600
        self.token_time = None

    def login(self):
        """
        Login to the spotify to get the access token and other related values
        """
        self.token_time = datetime.now()
        response = requests.post(self.token_api, auth=HTTPBasicAuth(self.client_id, self.client_secret),
                                 headers=self.headers, params=self.data)
        response = response.json()
        self.access_token = response.get('access_token')
        self.token_type = response.get('token_type')
        self.expires_in = response.get('expires_in')

    @property
    def token(self):
        return f'{self.token_type} {self.access_token}'

    def __call__(self, *args, **kwargs):
        now = datetime.now()
        if self.token_time is None or (now - self.token_time).total_seconds() > self.expires_in:
            self.login()
        return {"Authorization": self.token}


with open("../config.json") as file:
    config = json.load(file)

authorization = Authorization(**config)
