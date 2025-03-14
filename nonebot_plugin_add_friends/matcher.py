from nonebot.adapters.onebot.v11 import Bot, FriendRequestEvent, GroupRequestEvent, Message, PrivateMessageEvent
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command, on_request
from nonebot.rule import is_type

from .config import FriendRequest, GroupInviteRequest
from .event import get_friend_requests, get_group_invites, save_friend_requests, save_group_invites

# 注册请求处理
friend_add = on_request(priority=1)
group_invite = on_request(priority=1)


@friend_add.handle()
async def handle_friend_add(bot: Bot, event: FriendRequestEvent):
    """处理好友申请"""
    add_qq = event.user_id
    add_comment = event.comment or "无"
    add_flag = event.flag
    try:
        add_nickname: str = (await bot.get_stranger_info(user_id=event.user_id))["nickname"] or "未知昵称"
    except Exception:
        add_nickname: str = "未知昵称"
    logger.info(f"收到好友请求: QQ号{add_qq}，昵称{add_nickname}，验证消息{add_comment}")
    # 保存好友邀请
    friend_request = FriendRequest(
        add_id=add_qq,
        add_comment=add_comment,
        add_flag=add_flag,
        add_nickname=add_nickname,
    )
    friend_requests = await get_friend_requests()
    for i, req in enumerate(friend_requests.copy()):
        if req.add_id == add_qq:
            friend_requests.pop(i)
            logger.debug(f"移除已存在的好友申请: QQ号{add_qq}")
            break
    friend_requests.append(friend_request)
    await save_friend_requests(friend_requests)
    # 通知超级用户
    superusers = bot.config.superusers
    for su in superusers:
        msg = (
            f"收到新的好友申请：\n"
            f"昵称：{add_nickname}\n"
            f"QQ号：{add_qq}\n"
            f"验证信息：{add_comment}\n"
            f"使用命令“同意申请 {add_qq}”同意好友申请。\n"
            f"使用命令“拒绝申请 {add_qq}”拒绝好友申请。"
        )
        logger.info(f"向超级用户 {su} 发送好友请求消息")
        await bot.send_private_msg(user_id=int(su), message=msg)


@group_invite.handle()
async def handle_group_invite(bot: Bot, event: GroupRequestEvent):
    """处理群邀请"""
    if event.sub_type != "invite":
        return
    inviter_id = event.user_id
    inviter_group_id = event.group_id
    invite_comment = event.comment or "无"
    invite_flag = event.flag
    try:
        inviter_nickname: str = (await bot.get_stranger_info(user_id=event.user_id))["nickname"] or "未知昵称"
    except Exception:
        inviter_nickname: str = "未知昵称"
    try:
        inviter_groupname: str = (await bot.get_group_info(group_id=event.group_id))["group_name"] or "未知群名"
    except Exception:
        inviter_groupname: str = "未知群名"
    logger.info(
        f"收到群邀请：群号 {inviter_group_id}，群名称：{inviter_groupname}，"
        f"邀请人 {inviter_id}，邀请人昵称{inviter_nickname}，验证信息：{invite_comment}"
    )
    # 保存群邀请
    group_invite = GroupInviteRequest(
        add_id=inviter_id,
        add_group=inviter_group_id,
        add_comment=invite_comment,
        add_flag=invite_flag,
        add_nickname=inviter_nickname,
        add_groupname=inviter_groupname,
        sub_type=event.sub_type,
    )
    group_invites = await get_group_invites()
    for i, invite in enumerate(group_invites.copy()):
        if invite.add_group == inviter_group_id:
            group_invites.pop(i)
            logger.debug(f"移除已存在的群邀请: 群号{inviter_group_id}")
            break
    group_invites.append(group_invite)
    await save_group_invites(group_invites)
    # 通知超级用户
    superusers = bot.config.superusers
    for su in superusers:
        msg = (
            f"收到新的群邀请：\n"
            f"邀请人：{inviter_id}\n"
            f"邀请人昵称：{inviter_nickname}\n"
            f"群号：{inviter_group_id}\n"
            f"群名称：{inviter_groupname}\n"
            f"验证信息：{invite_comment}\n"
            f"使用命令“同意申请 {inviter_group_id}”同意群聊邀请。\n"
            f"使用命令“拒绝申请 {inviter_group_id}”拒绝群聊邀请。"
        )
        await bot.send_private_msg(user_id=int(su), message=msg)


# 创建命令 Matcher
view_requests = on_command("查看申请", rule=is_type(PrivateMessageEvent), permission=SUPERUSER, priority=1, block=True)
confirm_request = on_command(
    "同意申请", rule=is_type(PrivateMessageEvent), permission=SUPERUSER, priority=1, block=True
)
reject_request = on_command("拒绝申请", rule=is_type(PrivateMessageEvent), permission=SUPERUSER, priority=1, block=True)
all_confirm_requests = on_command(
    "同意全部申请", rule=is_type(PrivateMessageEvent), permission=SUPERUSER, priority=1, block=True
)
all_reject_requests = on_command(
    "拒绝全部申请", rule=is_type(PrivateMessageEvent), permission=SUPERUSER, priority=1, block=True
)
clear_requests = on_command(
    "清空申请列表", rule=is_type(PrivateMessageEvent), permission=SUPERUSER, priority=1, block=True
)


@view_requests.handle()
async def handle_view_requests(matcher: Matcher):
    """查看所有待处理的好友申请和群邀请"""
    friend_requests = await get_friend_requests()
    group_invites = await get_group_invites()
    if not friend_requests and not group_invites:
        await matcher.finish("当前没有待处理的好友申请或群邀请。")
    response = "待处理申请：\n"
    if friend_requests:
        response += "好友申请：\n"
        for req in friend_requests:
            response += f"昵称：{req.add_nickname}，QQ号：{req.add_id}，验证信息：{req.add_comment}\n"
    if group_invites:
        response += "群邀请：\n"
        for invite in group_invites:
            response += (
                f"邀请人：{invite.add_id}，邀请人昵称：{invite.add_nickname}，"
                f"群号：{invite.add_group}，群名称：{invite.add_groupname}，验证信息：{invite.add_comment}\n"
            )
    await matcher.finish(response)


@confirm_request.handle()
async def handle_confirm_request(bot: Bot, matcher: Matcher, arg: Message = CommandArg()):
    """通过命令同意好友申请或群邀请"""
    identifier = arg.extract_plain_text().strip()
    if not identifier:
        await matcher.finish("请输入申请的 QQ号 或 群号。")
    # 获取待处理的好友申请和群聊邀请
    friend_requests = await get_friend_requests()
    group_invites = await get_group_invites()
    # 查找并同意好友申请
    for req in friend_requests:
        if str(req.add_id) == identifier:
            await bot.set_friend_add_request(flag=req.add_flag, approve=True)
            friend_requests.remove(req)
            await save_friend_requests(friend_requests)
            await matcher.finish(f"已同意好友申请：{identifier}")
    # 查找并同意群聊邀请
    for invite in group_invites:
        if str(invite.add_group) == identifier:
            await bot.set_group_add_request(flag=invite.add_flag, sub_type=invite.sub_type, approve=True)
            group_invites.remove(invite)
            await save_group_invites(group_invites)
            await matcher.finish(f"已同意群邀请：{identifier}")
    await matcher.finish("未找到对应的好友申请或群邀请，请检查输入是否正确。")


@reject_request.handle()
async def handle_reject_request(bot: Bot, matcher: Matcher, arg: Message = CommandArg()):
    """通过命令拒绝好友申请或群邀请"""
    identifier = arg.extract_plain_text().strip()
    if not identifier:
        await matcher.finish("请输入要拒绝的 QQ号 或 群号。")
    # 获取待处理的好友申请和群聊邀请
    friend_requests = await get_friend_requests()
    group_invites = await get_group_invites()
    # 查找并拒绝好友申请
    for req in friend_requests:
        if str(req.add_id) == identifier:
            await bot.set_friend_add_request(flag=req.add_flag, approve=False)
            friend_requests.remove(req)
            await save_friend_requests(friend_requests)
            await matcher.finish(f"已拒绝好友申请：{identifier}")
    # 查找并拒绝群聊邀请
    for invite in group_invites:
        if str(invite.add_group) == identifier:
            await bot.set_group_add_request(flag=invite.add_flag, sub_type=invite.sub_type, approve=False)
            group_invites.remove(invite)
            await save_group_invites(group_invites)
            await matcher.finish(f"已拒绝群邀请：{identifier}")
    await matcher.finish("未找到对应的好友申请或群邀请，请检查输入是否正确。")


@all_confirm_requests.handle()
async def handle_all_confirm_requests(bot: Bot, matcher: Matcher):
    """同意所有待处理的好友申请和群邀请"""
    friend_requests = await get_friend_requests()
    group_invites = await get_group_invites()
    if not friend_requests and not group_invites:
        await matcher.finish("当前没有待处理的好友申请或群邀请。")
    confirm_friend_details = []
    confirm_group_details = []
    failed_friend_details = []
    failed_group_details = []
    # 处理好友申请
    for req in friend_requests.copy():
        try:
            await bot.set_friend_add_request(flag=req.add_flag, approve=True)
            confirm_friend_details.append(f"昵称：{req.add_nickname}，QQ号：{req.add_id}")
        except ActionFailed as e:
            logger.warning(f"同意好友申请失败：QQ号 {req.add_id}，错误：{e!s}")
            failed_friend_details.append(f"昵称：{req.add_nickname}，QQ号：{req.add_id}，错误：{e!s}")
        finally:
            friend_requests.remove(req)
    # 处理群邀请
    for invite in group_invites.copy():
        try:
            await bot.set_group_add_request(flag=invite.add_flag, sub_type=invite.sub_type, approve=True)
            confirm_group_details.append(f"群号：{invite.add_group}，群名称：{invite.add_groupname}")
        except ActionFailed as e:
            logger.warning(f"同意群邀请失败：群号 {invite.add_group}，错误：{e!s}")
            failed_group_details.append(f"群号：{invite.add_group}，群名称：{invite.add_groupname}，错误：{e!s}")
        finally:
            group_invites.remove(invite)
    # 保存更新后的空列表
    await save_friend_requests([])
    await save_group_invites([])
    # 构建详细的响应消息
    response = "已同意所有好友申请和群邀请：\n"
    if confirm_friend_details:
        response += "同意的好友申请：\n" + "\n".join(confirm_friend_details) + "\n"
    if confirm_group_details:
        response += "同意的群邀请：\n" + "\n".join(confirm_group_details)
    if failed_friend_details or failed_group_details:
        response += "\n同意失败的请求如下：\n"
        if failed_friend_details:
            response += "好友申请：\n" + "\n".join(failed_friend_details) + "\n"
        if failed_group_details:
            response += "群邀请：\n" + "\n".join(failed_group_details)
    await matcher.finish(response)


@all_reject_requests.handle()
async def handle_all_reject_requests(bot: Bot, matcher: Matcher):
    """拒绝所有待处理的好友申请和群邀请"""
    friend_requests = await get_friend_requests()
    group_invites = await get_group_invites()
    if not friend_requests and not group_invites:
        await matcher.finish("当前没有待处理的好友申请或群邀请。")
    reject_friend_details = []
    reject_group_details = []
    failed_friend_details = []
    failed_group_details = []
    # 处理好友申请
    for req in friend_requests.copy():
        try:
            await bot.set_friend_add_request(flag=req.add_flag, approve=False)
            reject_friend_details.append(f"昵称：{req.add_nickname}，QQ号：{req.add_id}")
        except ActionFailed as e:
            logger.warning(f"拒绝好友申请失败：QQ号 {req.add_id}，错误：{e!s}")
            failed_friend_details.append(f"昵称：{req.add_nickname}，QQ号：{req.add_id}，错误：{e!s}")
        finally:
            friend_requests.remove(req)
    # 处理群邀请
    for invite in group_invites.copy():
        try:
            await bot.set_group_add_request(flag=invite.add_flag, sub_type=invite.sub_type, approve=False)
            reject_group_details.append(f"群号：{invite.add_group}，群名称：{invite.add_groupname}")
        except ActionFailed as e:
            logger.warning(f"拒绝群邀请失败：群号 {invite.add_group}，错误：{e!s}")
            failed_group_details.append(f"群号：{invite.add_group}，群名称：{invite.add_groupname}，错误：{e!s}")
        finally:
            group_invites.remove(invite)
    # 保存更新后的空列表
    await save_friend_requests([])
    await save_group_invites([])
    # 构建详细的响应消息
    response = "已拒绝所有好友申请和群邀请：\n"
    if reject_friend_details:
        response += "拒绝的好友申请：\n" + "\n".join(reject_friend_details) + "\n"
    if reject_group_details:
        response += "拒绝的群邀请：\n" + "\n".join(reject_group_details)
    if failed_friend_details or failed_group_details:
        response += "\n拒绝失败的请求如下：\n"
        if failed_friend_details:
            response += "好友申请：\n" + "\n".join(failed_friend_details) + "\n"
        if failed_group_details:
            response += "群邀请：\n" + "\n".join(failed_group_details)
    await matcher.finish(response)


@clear_requests.handle()
async def handle_clear_requests(matcher: Matcher):
    """清空所有待处理的好友申请和群邀请"""
    # 获取当前的申请列表
    friend_requests = await get_friend_requests()
    group_invites = await get_group_invites()

    # 检查是否有待处理的申请
    if not friend_requests and not group_invites:
        await matcher.finish("当前没有待处理的好友申请或群邀请。")

    # 清空列表
    await save_friend_requests([])
    await save_group_invites([])

    # 返回简单的响应消息
    await matcher.finish("已清空申请列表。")
