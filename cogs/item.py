from discord.ext import commands
from dislash import slash_commands


class Item(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _item(self, ctx):
        await ctx.send("現在絶賛開発中...")
    
    @commands.command(name="item")
    async def c_item(self, ctx):
        await self._item(ctx)

    @slash_commands.command(description="お買い物をします。")
    async def item(self, inter):
        await self._item(inter)

def setup(bot):
    bot.add_cog(Item(bot))