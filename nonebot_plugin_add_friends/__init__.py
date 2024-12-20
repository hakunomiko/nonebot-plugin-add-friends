from nonebot.plugin import PluginMetadata

from .matcher import *

__plugin_meta__ = PluginMetadata(
    name="好友与群邀请管理",
    description="处理好友申请和群邀请，支持查看申请、手动同意/拒绝申请、同意/拒绝全部申请。",
    usage=(
        "1. 超级用户接收提醒消息。\n"
        "2. 私聊使用命令查看和管理申请：\n"
        "   - 查看申请：查看待处理申请。\n"
        "   - 同意申请 <QQ号/群号>：手动同意申请。\n"
        "   - 拒绝申请 <QQ号/群号>：手动拒绝申请。\n"
        "   - 同意/拒绝全部申请：同意/拒绝全部好友申请和群聊邀请。"
    ),
    type="application",
    homepage="https://github.com/hakunomiko/nonebot-plugin-add-friends",
    supported_adapters={"~onebot.v11"},
)
