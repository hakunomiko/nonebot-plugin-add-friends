import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Extra
from nonebot import require
require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store


class Config(BaseModel, extra=Extra.ignore):
    friend_path: Path = store.get_plugin_data_dir()


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
    def default(self, obj):
        if isinstance(obj, FriendRequest):
            return obj.dict()
        return super().default(obj)


class GroupInviteRequestEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GroupInviteRequest):
            return obj.dict()
        return super().default(obj)
