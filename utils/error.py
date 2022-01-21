import discord

def ErrorEmbed(title:str, description:str) -> discord.Embed:
    return discord.Embed(title=title, description=description, color=0xff0000)

def RequireFault() -> discord.Embed:
    return ErrorEmbed("エラー", "あなたはまだこのコマンドを使う条件を満たしていないようです...")