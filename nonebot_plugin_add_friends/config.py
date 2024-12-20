import json
from typing import Optional

from pydantic import BaseModel


class FriendRequest(BaseModel):
    add_id: int
    add_comment: Optional[str]
    add_flag: str
    add_nickname: str


class GroupInviteRequest(BaseModel):
    add_id: int
    add_group: int
    add_comment: Optional[str]
    add_flag: str
    add_nickname: str
    add_groupname: str
    sub_type: str


class FriendRequestEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, FriendRequest):
            return o.dict()
        return super().default(o)


class GroupInviteRequestEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, GroupInviteRequest):
            return o.dict()
        return super().default(o)
