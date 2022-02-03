import discord
from .easydb import EasyDB
from .easymenu import EasyMenu, EasyButton
from .error import ErrorEmbed, RequireFault

__all__ = [
    "EasyDB",
    "EasyMenu",
    "ErrorEmbed",
    "EasyButton",
    "RequireFault",
    "data_converter"
]

def data_converter(data:str, ctx:discord.ext.commands.Context) -> str:
    """dataをctxの情報をもとに変換します。
    変換できるもの
        ctx.author(.name[id])
        ctx.channel.name(id)
        ctx.guild.name(id)
    もし変換できなかった(guildがないなど)場合はNoneに置き換えます。
    data: str
        変換する元データ。fをつけてf-stringになるような形で記述してください。
    ctx: commands.Context
        ctxデータ。このデータから変換材料を抽出します。"""
    for m in ["author.name", "author.name", "author", "channel.id", "channel.name", "message.content"]:
        replacedata = ctx
        for s in m.split("."):
            replacedata = getattr(replacedata, s, None)
            if replacedata is None:
                break
        data = data.replace("{ctx."+m+"}", str(replacedata))
    return data