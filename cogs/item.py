from discord.ext import commands
from dislash import slash_commands
from utils import RequireFault
from json import dumps, loads

class Item(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _item(self, ctx):
        if self.bot.version in ["0.2", "0.3"]:
            # バージョンロック
            return await ctx.send("現在絶賛開発中...")
        userdata = self.bot.db.users[ctx.author.id][0]
        useritemdata = self.bot.db.item.search(user=ctx.author.id)[0][1]
        if userdata[2] < 5:
            return RequireFault(ctx)
        uitemdata = json.loads(useritemdata)

    @commands.command(name="item")
    async def c_item(self, ctx):
        await self._item(ctx)

    @slash_commands.command(description="自分の持っているアイテムの確認をします。")
    async def item(self, inter):
        await self._item(inter)


def setup(bot):
    bot.add_cog(Item(bot))