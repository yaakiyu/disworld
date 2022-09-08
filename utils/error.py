from discord.ext import commands
import discord


def ErrorEmbed(title:str, description:str, color=0xff0000) -> discord.Embed:
    "カラーがデフォルトで赤にされたEmbedを返します。"
    return discord.Embed(
        title=title,
        description=description,
        color=color
    )


async def RequireFault(ctx: commands.Context) -> discord.Message:
    "コマンド使用条件を満たしていないことを表示します。"
    return await ctx.send(embed=ErrorEmbed(
        "エラー",
        "あなたはまだこのコマンドを使う条件を満たしていないようです..."
    ))
