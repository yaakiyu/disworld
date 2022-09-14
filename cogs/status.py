# disworld - status

from discord.ext import commands


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _status(self, ctx: commands.Context):
        await self.bot.lock_checker(ctx, 5, 0.2)

    @commands.hybrid_command(name="status", aliases=["st", "stats"])
    async def c_status(self, ctx):
        await self._status(ctx)


async def setup(bot):
    await bot.add_cog(Status(bot))