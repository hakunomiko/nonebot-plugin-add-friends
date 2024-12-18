import json
from typing import List

from nonebot import get_plugin_config

from .config import Config, FriendRequest, FriendRequestEncoder, GroupInviteRequest, GroupInviteRequestEncoder

# 加载插件配置
plugin_config = get_plugin_config(Config)


# 确保目录存在
if not plugin_config.friend_path.exists():
    plugin_config.friend_path.mkdir(parents=True, exist_ok=True)


# 申请列表存储路径
friend_file = plugin_config.friend_path / "friend_requests.json"
group_invite_file = plugin_config.friend_path / "group_invites.json"


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
            cls=FriendRequestEncoder,
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
            cls=GroupInviteRequestEncoder,
            ensure_ascii=False,
            indent=4,
        )
