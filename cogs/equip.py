from discord.ext import commands
from dislash import slash_commands, OptionParam

class Equip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _equip(self, ctx, arg):
        # バージョンロック
        if self.bot.version == "0.2":
            return await ctx.send("主人公はまだ装備の仕方を知らない...")
        args = arg.aplit()
        
        if args[0] == "set":
            pass
        if args[0] == "set":
            pass

    @commands.command("equip")
    async def c_equip(self, ctx, *, arg=None):
        return await self._equip(ctx, arg)

    @slash_commands.command(description="装備を確認したり、装備したりします。")
    async def equip(self, inter, arg:str = OptionParam("None", desc="装備したいもの")):
        return await self._equip(inter, (arg if arg != "None" else None))

def setup(bot):
    bot.add_cog(Equip(bot))