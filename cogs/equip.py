from nextcord.ext import commands
from dislash import slash_commands

class Equip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _equip(self, ctx, arg):
        pass

    @commands.command("equip")
    async def c_equip(self, ctx, arg=None):
        return await self._equip(ctx, arg)

    @slash_commands.command(description="装備を確認したり、装備したりします。")
    async def equip(self, ctx):
        return await self._equip(ctx, None)

def setup(bot):
    bot.add_cog(Equip(bot))