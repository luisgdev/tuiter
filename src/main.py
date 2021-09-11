from typing import List
from tuiter import Tuiter


class TuiterList:
    def __init__(self, name: str, mode: str, description: str, ids: List[int]):
        self.id: int
        self.name = name
        self.mode = mode
        self.description = description
        self.ids = ids

    def _create(self):
        self.id = tw.create_list(self.name, self.mode, self.description)["id"]

    def update(self):
        self._create()
        cont: int = 0
        limit: int = 100
        n_ids: int = len(self.ids)
        res: dict = {}
        # ADD SEND THEM IN GROUPS OF 100 IDs (limit per request)
        groups: int = int(n_ids/limit) + (1 if n_ids%limit > 0 else 0)
        for _ in range(groups):
            sub_list: List[int] = self.ids[cont:cont+limit]
            res = tw.update_list(self.id, sub_list)
            cont += limit
        print(res)


# THIS PROGRAM WILL CREATE A TWITTER LIST
# TO ADD USERS YOU FOLLOW THAT DON'T FOLLOW YOU
if __name__ == "__main__":
    tw: Tuiter = Tuiter()
    # REQUEST your ´followers´ and ´friends´ LISTS
    print(f"HELLO @{tw.my_username}")
    followers: List[int] = tw.get_users_ids(tw.my_username, "followers")["ids"]
    friends: List[int] = tw.get_users_ids(tw.my_username, "friends")["ids"]
    print(f"FOLLOWING: {len(followers)}")
    print(f"FOLLOWERS: {len(friends)}")
    # FIND THOSE ´non_followers´ AND ´unknown_followers´
    non_followers: List[int] = list(set(friends) - set(followers))
    unknown_followers: List[int] = list(set(followers) - set(friends))
    # CREATE THE LISTS ON TWITTER 
    print(f"NON-FOLLOWERS: {len(non_followers)}")
    nf_list: TuiterList = TuiterList(
        name="Tuiter: Non-followers",
        mode="private",
        description="Accounts I follow who don't follow me.",
        ids=non_followers
    )
    nf_list.update()
    print(f"UNKNOWN-FOLLOWERS: {len(unknown_followers)}")
    uf_list: TuiterList = TuiterList(
        name="Tuiter: Unknown-followers",
        mode="private",
        description="Accounts who follow me and I don't follow.",
        ids=unknown_followers
    )
    uf_list.update()

