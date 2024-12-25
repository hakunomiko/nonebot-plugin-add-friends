import json
from pathlib import Path
from typing import List

from nonebot import require

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

from .config import FriendRequest, GroupInviteRequest

# 确保目录存在
friend_path: Path = store.get_plugin_data_dir()
if not friend_path.exists():
    friend_path.mkdir(parents=True, exist_ok=True)


# 申请列表存储路径
friend_file = friend_path / "friend_requests.json"
group_invite_file = friend_path / "group_invites.json"


async def get_friend_requests() -> List[FriendRequest]:
    """获取好友申请列表"""
    try:
        with friend_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return [FriendRequest(**item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


async def save_friend_requests(friend_requests: List[FriendRequest]) -> None:
    """存储好友申请列表"""
    with friend_file.open("w", encoding="utf-8") as f:
        json.dump(
            [request.dict() for request in friend_requests],
            f,
            ensure_ascii=False,
            indent=4,
        )


async def get_group_invites() -> List[GroupInviteRequest]:
    """获取群聊邀请列表"""
    try:
        with group_invite_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return [GroupInviteRequest(**item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


async def save_group_invites(group_invites: List[GroupInviteRequest]) -> None:
    """存储群聊邀请列表"""
    with group_invite_file.open("w", encoding="utf-8") as f:
        json.dump(
            [invite.dict() for invite in group_invites],
            f,
            ensure_ascii=False,
            indent=4,
        )
