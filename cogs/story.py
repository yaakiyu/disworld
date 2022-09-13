from discord.ext import commands
import discord
# from dislash import slash_commands
import utils

from core import Bot


class Story(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _story(self, ctx):
        if ctx.author.id not in self.bot.db.user:
            self.bot.db.user.insert((ctx.author.id, "", 0, 0, 0, 0, 0))
        userdata = self.bot.db.user[ctx.author.id]["Story"]
        opt = {"エピソード1「始まらなかった話」":"1"}
        if userdata >= 2:
            opt["エピソード2「初めてのおつかい」"] = "2"
        if userdata >= 4 and self.bot.version == "0.3":
            opt["エピソード3「いざ、対決！」"] = "3"
        if userdata >= 7 and self.bot.version == "0.4":
            opt["エピソード4「」"] = "4"

        e=discord.Embed(title="エピソード - 選択", description="見たいエピソードを選んでください。")
        menu = utils.EasyMenu("story", "選択してください", **opt)
        msg = await ctx.send(embed=e, components=[menu])
        inter = await msg.wait_for_dropdown(lambda i:i.author == ctx.author)
        label = int(inter.select_menu.selected_options[0].value)
        storydata = self.bot.storydata["1"][str(label)]["ja"]

        if label == 1 and userdata == 0:
            self.bot.db.users.update_item(f"id={ctx.author.id}", story=1)
        elif label == 2 and userdata == 2:
            self.bot.db.users.update_item(f"id={ctx.author.id}", story=3)
        elif label == 3 and userdata == 4:
            self.bot.db.users.update_item(f"id={ctx.author.id}", story=5)
        elif label == 4 and userdata == 7:
            self.bot.db.users.update_item(f"id={ctx.author.id}", story=8)
        e = discord.Embed(title=f"Ep.{label}", description=storydata)
        await msg.edit(embed=e, components=[])

#    @slash_commands.command(description="ストーリーです。")
#    async def story(self, inter):
#        await self._story(inter)

    @commands.command(name="story")
    async def c_story(self, ctx):
        await self._story(ctx)


async def setup(bot: Bot):
    await bot.add_cog(Story(bot))