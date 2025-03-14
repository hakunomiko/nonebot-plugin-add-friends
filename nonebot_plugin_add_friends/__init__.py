from nonebot.plugin import PluginMetadata

from .matcher import *

__plugin_meta__ = PluginMetadata(
    name="好友与群邀请管理",
    description="处理好友申请和群邀请，支持查看申请、手动同意或拒绝申请、以及同意或拒绝全部申请。",
    usage=(
        "1. 超级用户将会收到提醒消息。\n"
        "2. 您可以通过私聊使用以下命令来查看和管理申请：\n"
        "   - 查看申请：查看所有待处理的申请。\n"
        "   - 同意申请 <QQ号/群号>：手动同意指定QQ号的好友申请或群号的入群邀请。\n"
        "   - 拒绝申请 <QQ号/群号>：手动拒绝指定QQ号的好友申请或群号的入群邀请。\n"
        "   - 同意/拒绝全部申请：同意或拒绝所有的好友申请和群聊邀请。\n"
        "   - 清空申请列表：直接清空存储的申请列表，不执行同意或拒绝操作。\n"
        "   ⚠️ 注意：清空申请列表会清除插件记录的全部申请，后续若需要同意或拒绝，请手动操作。"
    ),
    type="application",
    homepage="https://github.com/hakunomiko/nonebot-plugin-add-friends",
    supported_adapters={"~onebot.v11"},
)
