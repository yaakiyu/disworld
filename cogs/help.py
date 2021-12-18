from discord.ext import commands
import discord
from dislash import slash_commands, Option

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _help(self, ctx, command):
        if not ctx.author.id in self.bot.owner_ids:
            # 公開前限定：オーナー専用ロック
            return await ctx.send("I wont help you!!")
        if command is None:pass

    @slash_commands.command(
        description="このbotのヘルプ",
        options=[Option("command", "詳しくhelpを見たいコマンド", required=False)]
    )
    async def help(self, inter, command=None):
        await self._help(inter, command)

    @commands.command(name="help")
    async def c_help(self, ctx, command=None):
        await self._help(ctx, command)

def setup(bot):
    bot.add_cog(Help(bot))