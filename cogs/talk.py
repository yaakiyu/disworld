from discord.ext import commands
import discord

import utils
from core import Bot


class Talk(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _talk(self, ctx):
        await self.bot.lock_checker(ctx, 6)
        udata = self.bot.db.user[ctx.author.id]["Story"]
        if udata <= 2:
            opt = {"老人":"1"}
        else:
            opt = {}
        if opt == {}:
            return await ctx.send(embed=utils.ErrorEmbed("エラー", "現在話せる相手がいません！"))
        e = discord.Embed(title="talk - 選択", description="誰と話すか決めてください。")
        menu = utils.EasyMenu("話し相手", "選択してください", **opt)
        msg = await ctx.send(embed=e, components=[menu])
        inter = await msg.wait_for_dropdown(lambda i:i.author == ctx.author)

        if label:=int(inter.select_menu.selected_options[0].value) == 1:
            talk = self.bot.talkdata["1"]["ja"]
            if self.bot.db.user[ctx.author.id]["Story"] == 1:
                self.bot.db.user[ctx.author.id]["Story"] = 2
            e = discord.Embed(title="老人に話しかけた。",description=utils.data_converter(talk, ctx))
        await msg.edit(embed=e,components=[])

#    @slash_commands.command(description="指定した人と会話する。")
#    async def talk(self, inter):
#        await self._talk(inter)

    @commands.command(name="talk")
    async def c_talk(self, ctx):
        await self._talk(ctx)


async def setup(bot):
    await bot.add_cog(Talk(bot))