from nextcord.ext import commands
import nextcord as discord
from dislash import slash_commands
import utils

class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _talk(self, ctx):
        if not self.bot.db.users.is_in(id=ctx.author.id):
            return await ctx.send("あなたはゲームを始めていません！storyコマンドでゲームを開始してください！")
        if (udata:=self.bot.db.users.search(id=ctx.author.id)[0][2]) < 1:
            return await utils.RequireFault(ctx)
        e = discord.Embed(title="talk - 選択", description="誰と話すか決めてください。")
        if udata <= 2:
            opt = {"老人":"1"}
        else:
            opt = {}
        if opt == {}:
            return await ctx.send(embed=util.ErrorEmbed("エラー", "現在話せる相手がいません！"))
        menu = utils.EasyMenu("話し相手", "選択してください", **opt)
        msg = await ctx.send(embed=e, components=[menu])
        inter = await msg.wait_for_dropdown(lambda i:i.author == ctx.author)

        if label:=int(inter.select_menu.selected_options[0].value) == 1:
            talk = self.bot.talkdata["1"]["ja"]
            if self.bot.db.users.search(id=ctx.author.id)[0][2] == 1:
                self.bot.db.users.update_item(f"id={ctx.author.id}", story=2)
            e = discord.Embed(title="老人に話しかけた。",description=utils.data_converter(talk, ctx))
        await msg.edit(embed=e,components=[])

    @slash_commands.command(description="指定した人と会話する。")
    async def talk(self, inter):
        await self._talk(inter)

    @commands.command(name="talk")
    async def c_talk(self, ctx):
        await self._talk(ctx)


def setup(bot):
    bot.add_cog(Talk(bot))