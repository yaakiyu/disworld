# disworld - talk

from discord.ext import commands
import discord

import utils
from core import Bot


class TalkView(discord.ui.View):

    def __init__(self, bot: Bot, options, ctx: commands.Context):
        self.bot = bot
        super().__init__()
        self.story_select.options = utils.EasyOption(
            **options
        )
        self.ctx = ctx

    @discord.ui.select(
        placeholder="選択してください...",
        options=[]
    )
    async def story_select(
        self, inter: discord.Interaction, select: discord.ui.Select
    ):
        e = utils.ErrorEmbed("エラー", "不明なエラーが発生しました。")
        if int(select.values[0]) == 1:
            talk = self.bot.talkdata["1"]["ja"]
            if self.bot.db.user[inter.user.id]["Story"] == 1:
                self.bot.db.user[inter.user.id]["Story"] = 2
            e = discord.Embed(
                title="老人に話しかけた。",
                description=utils.data_converter(talk, self.ctx)
            )
        await inter.response.edit_message(embed=e, view=None)


class Talk(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(descripotion="近くの人と話します。")
    async def talk(self, ctx):
        await self.bot.lock_checker(ctx, 1)
        udata = self.bot.db.user[ctx.author.id]["Story"]
        if udata <= 2:
            opt = {"老人":"1"}
        else:
            opt = {}
        if not opt:
            return await ctx.send(embed=utils.ErrorEmbed("エラー", "現在話せる相手がいません！"))
        e = discord.Embed(title="talk - 選択", description="誰と話すか決めてください。")
        await ctx.send(embed=e, view=TalkView(self.bot, opt, ctx))


async def setup(bot):
    await bot.add_cog(Talk(bot))