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
