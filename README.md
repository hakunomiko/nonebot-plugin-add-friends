<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-add-friends

_✨ 处理好友申请和群邀请，支持查看申请、手动同意/拒绝申请、同意/拒绝全部申请。 ✨_


<a href="https://github.com/hakunomiko/nonebot-plugin-add-friends/stargazers">
        <img alt="GitHub stars" src="https://img.shields.io/github/stars/hakunomiko/nonebot-plugin-add-friends" alt="stars">
</a>
<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/hakunomiko/nonebot-plugin-add-friends.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-add-friends">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-add-friends.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

此插件用于远程处理好友申请和加群邀请，支持查看申请、手动同意/拒绝申请、同意/拒绝全部申请。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-add-friends

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-add-friends
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-add-friends
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-add-friends
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-add-friends
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_add_friends"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| SUPERUSERS | 是 | 无 | Bot的超级用户，用于接收、同意/拒绝好友申请及群邀请信息。 |

## 🕹️ 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 查看申请 | 主人 | 否 | 私聊 | 查看待处理申请 |
| 同意/拒绝申请 <QQ号/群号> | 主人 | 否 | 私聊 | 同意/拒绝申请 |
| 同意/拒绝全部申请 | 主人 | 否 | 私聊 | 同意/拒绝全部申请 |

## 🎉 鸣谢
感谢以下开发者对本插件作出的贡献：
[Agnes4m](https://github.com/Agnes4m/nonebot_plugin_friends)
