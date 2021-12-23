from discord.ext import commands
import discord
from dislash import slash_commands
import utils

class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _data_convert(self, data, ctx):
        for m in ["author.name", "author.name", "channel.id", "channel.name"]:
            replacedata = ctx
            for s in m.split("."):
                replacedata = getattr(replacedata, s)
            data = data.replace("{ctx."+m+"}", str(replacedata))
        return data

    async def _talk(self, ctx):
        if not ctx.author.id in self.bot.owner_ids:
            return await ctx.send("未完成...")
        if not self.bot.db.users.is_in(id=ctx.author.id):
            return await ctx.send("あなたはゲームを始めていません！storyコマンドでゲームを開始してください！")
        if udata:=self.bot.db.users.search(id=ctx.author.id)[0][2] < 1:
            return await ctx.send("あなたはこのコマンドを使う条件を満たしていないようです...")
        e = discord.Embed(title="talk - 選択", description="誰と話すか決めてください。")
        if udata <= 2:
            opt = {"老人":"1"}
        menu = utils.EasyMenu("話し相手", "選択してください", **opt)
        msg = await ctx.send(embed=e, components=[menu])
        inter = await msg.wait_for_dropdown(lambda i:i.author == ctx.author)

        if label:=int(inter.select_menu.selected_options[0].value) == 1:
            talk = self.bot.talkdata["1"]["ja"]
            if self.bot.db.users.search(id=ctx.author.id)[0][2] == 1:
                self.bot.db.users.update_item(f"id={ctx.author.id}", story=2)
            e = discord.Embed(title="老人に話しかけた。",description=self._data_convert(talk, ctx))
        await msg.edit(embed=e,components=[])

    @slash_commands.command(description="指定した人と会話する。")
    async def talk(self, inter):
        await self._talk(inter)

    @commands.command(name="talk")
    async def c_talk(self, ctx):
        await self._talk(ctx)


def setup(bot):
    bot.add_cog(Talk(bot))