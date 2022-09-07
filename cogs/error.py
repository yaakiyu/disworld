from discord.ext import commands
import discord
import traceback


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        embed = discord.Embed(title="エラー", description="", color=0xff0000)
        if isinstance(e, commands.CommandNotFound):
            return
        elif isinstance(e, commands.NotOwner):
            embed.description = "あなたはこのコマンドを実行する権限がありません。"
        elif isinstance(e, commands.MemberNotFound):
            embed.description = f"指定されたメンバー{e.argument}が見つかりませんでした。"
        elif isinstance(e, commands.ChannelNotFound):
            embed.description = f"指定されたチャンネル{e.argument}がみつかりませんでした。"
        elif isinstance(e, commands.RoleNotFound):
            embed.description = "エラー", f"指定されたロール{e.argument}が見つかりませんでした。"
        elif isinstance(e, commands.EmojiNotFound):
            embed.description = f"指定された絵文字{e.argument}が見つかりませんでした。"
        elif isinstance(e, commands.MissingPermissions):
            embed.description = "あなたの権限が足りません。足りない権限：\n" + "\n".join(
                [str(m) for m in e.missing_perms])
        elif isinstance(e, commands.BotMissingPermissions):
            embed.description = "Botに権限が足りません。足りない権限：\n" + "\n".join(
                [str(m) for m in e.missing_perms])
        elif isinstance(e, commands.CommandOnCooldown):
            embed.description = f"このコマンドはクールダウン中です！\n{round(e.retry_after)}秒後に試してください！"
        elif isinstance(e, commands.ChannelNotReadable):
            embed.description = f"指定されたチャンネル({e.argument.mention})のメッセージを読む権限がありません。"
        elif isinstance(e, commands.InvalidEndOfQuotedStringError):
            embed.description = '`"`が閉じた後に空白なしで言葉が続いています。'
        elif isinstance(e, commands.PrivateMessageOnly):
            embed.description = "このコマンドはDM専用です！"
        elif isinstance(e, commands.NoPrivateMessage):
            embed.description = "このコマンドはDMでは使えません！"
        elif isinstance(e, commands.MissingRequiredArgument):
            embed.description = f"必要な引数({e.param})が足りません。"
        else:
            traceback.print_exception(type(e), e, e.__traceback__)
            error_msg = "```py\n" + "".join(
                traceback.format_exception(type(e), e,
                                           e.__traceback__)) + "\n```"
            await self.bot.get_channel(814830540133498920).send(
                f"""発生サーバー：{ctx.guild.name}(ID:{ctx.guild.id})
                    発生チャンネル：{ctx.channel.name}(ID:{ctx.channel.id})
                    発生ユーザー：{ctx.author}(ID:{ctx.author.id})
                    発生コマンド：{ctx.command.name}(`{ctx.message.content}`)""",
                embed=discord.Embed(
                    title="エラー詳細",
                    description=f"{error_msg}"
                )
            )
            return await ctx.send(
                embed=discord.Embed(
                    title="予期せぬエラーが発生しました",
                    description=error_msg + "開発者に報告してください。"
                )
            )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Error(bot))
