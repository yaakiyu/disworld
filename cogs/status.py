from discord.ext import commands
from dislash import slash_commands
import utils

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _status(self, ctx):
        if self.bot.version in ["0.1", "0.2"]:
            # バージョンロック
            await ctx.reply("ステータスなんて存在しない。")
        udata = self.bot.db.users[ctx.author.id][0][2]
        if udata < 5:
            return await ctx.send(embed=utils.RequireFault())
        if udata == 5:
            pass

    @slash_commands.command(description="あなたのステータスを見ることができます")
    async def status(self, inter):
        await self._status(inter)

    @commands.command(name="status", aliases=["st", "stats"])
    async def c_status(self, ctx):
        await self._status(ctx)


def setup(bot):
    bot.add_cog(Status(bot))