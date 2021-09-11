import json
import requests
from os import environ as env

from typing import List, Any
from requests_oauthlib import OAuth1
from dotenv import load_dotenv


load_dotenv()


class Tuiter():
    def __init__(self):
        self.base_url: str = "https://api.twitter.com"
        self.oauth = OAuth1(
            env["CONSUMER_KEY"],
            env["CONSUMER_SECRET"],
            env["ACCESS_TOKEN"],
            env["ACCESS_TOKEN_SECRET"]
        )
        self.my_username : str = self._get_me()

    def _get_me(self) -> str:
        url: str = f"{self.base_url}/1.1/account/settings.json"
        response = requests.get(url, auth=self.oauth)
        return json.loads(response.content)["screen_name"]

    def post_tweet(self, text: str) -> dict:
        # TO POST A TWEET
        params: dict = {"status": text}
        url: str = f"{self.base_url}/1.1/statuses/update.json"
        response = requests.post(url, auth=self.oauth, params=params)
        return json.loads(response.content)

    def get_user(self, username: str) -> dict:
        # TO GET THE USER OBJECT OF THE GIVEN USERNAME
        params: dict[str, str] = {"screen_name": username}
        url: str = f"{self.base_url}/1.1/users/show.json"
        response = requests.get(url, auth=self.oauth, params=params)
        return json.loads(response.content)

    def get_users_ids(self, username: str, target: str) -> dict:
        # TO GET LISTS OF FRIENDS IDS OR FOLLOWERS IDS
        if target not in ["followers", "friends"]:
            return {"Error": "target should be 'followers' or 'friends'."}
        params = {"screen_name":username, "cursor":-1, "stringify_ids": True}
        url: str = f"{self.base_url}/1.1/{target}/ids.json"
        response = requests.get(url, auth=self.oauth, params=params)
        return json.loads(response.content)

    def create_list(self, name: str, mode: str, description: str) -> dict:
        # CREATE A NEW TWITTER LIST
        params: dict = {"name": name, "mode": mode, "description": description}
        url: str = f"{self.base_url}/1.1/lists/create.json"
        response = requests.post(url, auth=self.oauth, params=params)
        return json.loads(response.content)

    def update_list(self, list_id: int, ids: List[Any]) -> dict:
        # UPDATE AN EXISTING TWITTER LIST(LIMIT 100)
        params: dict = {"list_id": list_id,"user_id": ','.join(map(str, ids))}
        url: str = f"{self.base_url}/1.1/lists/members/create_all.json"
        response = requests.post(url, auth=self.oauth, params=params)
        return json.loads(response.content)

    def search(self, username: str, count: int = 1) -> dict:
        # GET N TWEETS FROM GIVEN USER
        params: dict = {"q": username,"result_type": "recent","count": count}
        url: str = f"{self.base_url}/1.1/search/tweets.json"
        response = requests.get(url, auth=self.oauth, params=params)
        return json.loads(response.content)

    def friends_lookup(self, ids: List[Any]) -> dict:
        # GET FRIENDSHIP INFORMATION OF EVERY USER IN LIST(LIMIT 100)
        params: dict = {"user_id": ",".join(ids)}
        url: str = f"{self.base_url}/1.1/friendships/lookup.json"
        response = requests.get(url, auth=self.oauth, params=params)
        return json.loads(response.content)

if __name__ == '__main__':
    print('This is not Main!')
    tw = Tuiter()
    print(tw.my_username)
