import discord

def ErrorEmbed(title:str, description:str) -> discord.Embed:
    return discord.Embed(title=title, description=description, color=0xff0000)