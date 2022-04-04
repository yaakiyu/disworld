import discord

def ErrorEmbed(title:str, description:str, color=0xff0000) -> discord.Embed:
    return discord.Embed(
        title=title,
        description=description,
        color=color
    )

async def RequireFault(ctx: discord.ext.commands.Context) -> discord.Message:
    return await ctx.send(
        embed=ErrorEmbed(
            "エラー",
            "あなたはまだこのコマンドを使う条件を満たしていないようです..."
        )
    )