from discord.ext import commands
import discord
from dislash import slash_commands
import utils

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _shop(self, ctx):
        if self.bot.version == "0.1":
            return await ctx.send("現在コマンド絶賛開発中...")
        if not self.bot.db.users.is_in(id=ctx.author.id):
            return await ctx.send("あなたはゲームを始めていません！storyコマンドでゲームを開始してください！")
        if (udata:=self.bot.db.users.search(id=ctx.author.id)[0][2]) < 3:
            return await ctx.send("あなたはこのコマンドを使う条件を満たしていないようです...")
        if udata == 3:
            e = discord.Embed(title="ショップ - チュートリアル", description="...")
            menu = utils.EasyMenu("お店を選択", "お店を選択してください", **{"セーフイ生活店":"1"})
            msg = await ctx.send(embed=e, components=[menu])
            inter = await msg.wait_for_dropdown(lambda i:i.author == ctx.author)
            e = discord.Embed(title="セーフイ生活店 - チュートリアル", description="...")
            menu = utils.EasyMenu("アイテムを選択", "アイテムを選択してください", **{"ただの棒":"1"})
            await msg.edit(embed=e, components=[menu])
            inter = await msg.wait_for_dropdown(lambda i:i.author == ctx.author)
            e = discord.Embed(title="セーフイ生活店 - チュートリアル", description="(チュートリアル完了)")
            await msg.edit(embed=e, components=[])
            return self.bot.db.users.update_item(f"id={ctx.author.id}", story=4)


    @slash_commands.command(description="お買い物をします。")
    async def shop(self, inter):
        await self._shop(inter)


    @commands.command(name="shop")
    async def c_shop(self, ctx):
        await self._shop(ctx)


def setup(bot):
    bot.add_cog(Shop(bot))