# disworld - story

from discord.ext import commands
import discord

import utils

from core import Bot


class StoryView(discord.ui.View):

    def __init__(self, bot: Bot, options):
        self.bot = bot
        self.add_item(StorySelect(bot, utils.EasyOption(
            **options
        )))

class StorySelect(discord.ui.Select):
    def __init__(self, bot: Bot, options):
        self.bot = bot
        super().__init__(placeholder="ストーリー選択...", options=options)

    async def callback(
        self, inter: discord.Interaction
    ):
        label = int(self.values[0])
        userdata = self.bot.db.user[inter.user.id]["Story"]
        storydata = self.bot.storydata["1"][str(label)]["ja"]

        if (label, userdata) in ((1, 0), (2, 2), (3, 4), (4, 7)):
            self.bot.db.user[inter.user.id]["Story"] += 1
        e = discord.Embed(title=f"Ep.{label}", description=storydata)
        await inter.response.edit_message(embed=e, view=None)


class Story(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(description="ストーリーを見ます。")
    async def story(self, ctx):
        if ctx.author.id not in self.bot.db.user:
            self.bot.db.user.insert((ctx.author.id, "", 0, 0, 0, 0, 0))

        userdata = self.bot.db.user[ctx.author.id]["Story"]
        opt = {"エピソード1「始まらなかった話」":"1"}
        if userdata >= 2:
            opt["エピソード2「初めてのおつかい」"] = "2"
        if userdata >= 4 and self.bot.version_number > 0.2:
            opt["エピソード3「いざ、対決！」"] = "3"
        if userdata >= 7 and self.bot.version_number > 0.3:
            opt["エピソード4「」"] = "4"

        e = discord.Embed(
            title="エピソード - 選択",
            description="見たいエピソードを選んでください。"
        )
        await ctx.send(embed=e, view=StoryView(self.bot, opt))


async def setup(bot: Bot):
    await bot.add_cog(Story(bot))
