from discord.ext import commands
from discord.ext import commands
from dislash import slash_commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _status(self, ctx):
        await ctx.reply("ステータスなんて存在しない。")

    @slash_commands.command(description="あなたのステータスを見ることができます")
    async def status(self, inter):
        await self._status(inter)

    @commands.command(name="status", aliases=["st", "stats"])
    async def c_status(self, ctx):
        await self._status(ctx)


def setup(bot):
    bot.add_cog(Status(bot))