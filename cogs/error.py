from nextcord.ext import commands
import nextcord as discord
import traceback
import utils

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if isinstance(e, commands.CommandNotFound):
            return
        elif isinstance(e, commands.NotOwner):
            await ctx.send(embed=utils.ErrorEmbed("エラー", "あなたはこのコマンドを実行する権限がありません。"))
        elif isinstance(e, commands.MemberNotFound):
            await ctx.send(embed=utils.ErrorEmbed("エラー", f"指定されたメンバー{e.argument}が見つかりませんでした。"))
        elif isinstance(e, commands.ChannelNotFound):
            await ctx.send(embed=utils.ErrorEmbed("エラー", f"指定されたチャンネル{e.argument}がみつかりませんでした。"))
        elif isinstance(e, commands.RoleNotFound):
            await ctx.send(embed=utils.ErrorEmbed("エラー",f"指定されたロール{e.argument}が見つかりませんでした。"))
        elif isinstance(e, commands.EmojiNotFound):
            await ctx.send(embed=utils.ErrorEmbed("エラー",f"指定された絵文字{e.argument}が見つかりませんでした。"))
        elif isinstance(e, commands.MissingPermissions):
            await ctx.send(embed=utils.ErrorEmbed("エラー","あなたの権限が足りません。"))
        elif isinstance(e, commands.BotMissingPermissions):
            await ctx.send(embed=utils.ErrorEmbed("エラー","Botに権限が足りません。"))
#        elif isinstance(e, commands.DisableCommand):
#            await ctx.send(embed=utils.ErrorEmbed("エラー","このコマンドは無効化されています。"))
        elif isinstance(e, commands.CommandOnCooldown):
            await ctx.send(embed=utils.ErrorEmbed("エラー",f"このコマンドはクールダウン中です！\n{round(e.retry_after)}秒後に試してください！"))
        elif isinstance(e, commands.ChannelNotReadable):
            await ctx.send(embed=utils.ErrorEmbed("エラー",f"指定されたチャンネル({e.argument.mention})のメッセージを読む権限がありません。"))
        elif isinstance(e, commands.InvalidEndOfQuotedStringError):
            await ctx.send(embed=utils.ErrorEmbed("エラー",'`"`が閉じた後に空白なしで言葉が続いています。'))
        elif isinstance(e, commands.PrivateMessageOnly):
            await ctx.send(embed=utils.ErrorEmbed("エラー","このコマンドはDM専用です！"))
        elif isinstance(e, commands.NoPrivateMessage):
            await ctx.send(embed=utils.ErrorEmbed("エラー","このコマンドはDMでは使えません！"))
        elif isinstance(e, commands.MissingRequiredArgument):
            await ctx.send(embed=utils.ErrorEmbed("エラー",f"必要な引数({e.param})が足りません。"))
        else:
            traceback.print_exception(type(e), e, e.__traceback__)
            await ctx.send(embed=discord.Embed(title="エラーが発生しました", description="\n```py\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__))+ "\n```開発者に報告してください。"))


def setup(bot):
    bot.add_cog(Error(bot))