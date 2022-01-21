import discord

def ErrorEmbed(title:str, description:str) -> discord.Embed:
    return discord.Embed(title=title, description=description, color=0xff0000)

async def RequireFault(ctx: discord.ext.commands.Context) -> discord.Message:
    return await ctx.send(embed=ErrorEmbed("エラー", "あなたはまだこのコマンドを使う条件を満たしていないようです..."))