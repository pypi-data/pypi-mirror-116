import json.decoder
from utils import NotFoundError

import requests


class BrawlStarsAPIClient:
    def __init__(self, token):
        self.token = token
        self.apiurl = "https://api.brawlstars.com/v1/"
        self.playersendpoint = self.apiurl + "players"
        self.clubendpoint = self.apiurl + "clubs"

    def get_player(self, player_id):
        """Get data about player"""
        endpoint = f"{self.playersendpoint}/%23{player_id}"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(endpoint, headers=headers).json()
            return response
        except json.decoder.JSONDecodeError as jderr:
            raise NotFoundError

    def get_player_battlelog(self, player_id):
        """Get data about player's battle"""
        endpoint = f"{self.apiurl}players/%23{player_id}/battlelog"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(endpoint, headers=headers).json()
            return response
        except json.decoder.JSONDecodeError as jderr:
            raise NotFoundError

    def get_club_members(self, club_id, before, after, limit):
        """Get data about club's members"""
        endpoint = f"{self.clubendpoint}/%23{club_id}/members?before={before}&after={after}&limit={limit}"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(endpoint, headers=headers).json()
            return response
        except json.decoder.JSONDecodeError as jderr:
            raise NotFoundError

    def get_club(self, club_id):
        """Get data about club"""
        endpoint = f"{self.clubendpoint}/%23{club_id}"
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        try:
            response = requests.get(endpoint, headers=headers).json()
            return response
        except json.decoder.JSONDecodeError as jderr:
            raise NotFoundError
