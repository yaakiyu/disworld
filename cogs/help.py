from discord.ext import commands
import discord
from dislash import slash_commands, Option

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _help(self, ctx, command):
        if not ctx.author.id in self.bot.owner_ids:
            # 公開前限定：オーナー専用ロック
            return await ctx.send("I wont help you!!")
        if command is None:
            e = discord.Embed(title="Help", description="このbotのコマンドの紹介。")
            if not self.bot.db.users.is_in(id=ctx.author.id):
                e.add_field(name="story", value="最初は必ずこのコマンドを使ってください。")
            elif (user:=self.bot.db.users.search(id=ctx.author.id)[0][2]) == 0:
                e.add_field(name="story", value="最初は必ずこのコマンドを使ってください。")
            else:
                e.add_field(name="story", value="ストーリーを見ることができます。")
            if user >= 1:
                e.add_field(name="talk", value="ゲーム内のキャラと会話することができます")
            await ctx.send(embed=e)
        else:
            e = discord.Embed(title=f"help - {command}", description="** **")
            if command == "story":
                e.add_field(name="説明", value="このコマンドではbotのストーリーを見ることができます。このコマンドを使って、ミッションをクリアしていくことで、")

    @slash_commands.command(
        description="このbotのヘルプ",
        options=[Option("command", "詳しくhelpを見たいコマンド", required=False)]
    )
    async def help(self, inter, command=None):
        await self._help(inter, command)

    @commands.command(name="help")
    async def c_help(self, ctx, command=None):
        await self._help(ctx, command)

def setup(bot):
    bot.add_cog(Help(bot))