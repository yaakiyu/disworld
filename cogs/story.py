from discord.ext import commands
import discord
from dislash import slash_commands
import utils

class Story(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _story(self, ctx):
        if not ctx.author.id in self.bot.owner_ids:
            # 公開前限定：オーナー専用ロック
            return await ctx.reply("今はない。")
        if not self.bot.db.users.is_in(id=ctx.author.id):
            self.bot.db.users.add_item(ctx.author.id, "", 0, 0, 0, "")
        if self.bot.version == "0.1":
            opt = {"エピソード1「始まらなかった話」":"1"}
        elif self.bot.version == "0.2":
            opt = {"エピソード1「始まらなかった話」":"1", "エピソード2「」":"2"}
        e=discord.Embed(title="エピソード - 選択", description="見たいエピソードを選んでください。")
        menu = utils.EasyMenu("story", "選択してください", **opt)
        msg = await ctx.send(embed=e, components=[menu])
        inter = await msg.wait_for_dropdown(lambda i:i.author == ctx.author)

        if label:=int(inter.select_menu.selected_options[0].value) == 1:
            if self.bot.db.users.search(id=ctx.author.id)[0][2] == 0:
                self.bot.db.users.update_item(f"id={ctx.author.id}", story=1)
            e = discord.Embed(title="Ep.1",description="""
目覚めたら、見たこともないところに来た。果たしてここはどこなのか。
見回してみると、老人がいた。話すといいかもしれない。
```diff
ミッション
+ 「g.talk」で老人と話そう。
```""")

        elif label == 2:
            if self.bot.db.users.search(id=ctx.author.id)[0][2] == 2:
                self.bot.db.users.update_item(f"id={ctx.author.id}", story=3)
            e = discord.Embed(title="Ep.2", description="""
(story)
```diff
ミッション
+ (mission)
```""")
        await msg.edit(embed=e, components=[])

    @slash_commands.command(description="ストーリーです。")
    async def story(self, inter):
        await self._story(inter)

    @commands.command(name="story")
    async def c_story(self, ctx):
        await self._story(ctx)


def setup(bot):
    bot.add_cog(Story(bot))