from discord.ext import commands
import discord
from dislash import slash_commands, Option

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _help(self, ctx, command):
        if command is None:
            user = self.bot.db.users.search(id=ctx.author.id)[0][2]
            e = discord.Embed(title="Help", description="このbotのコマンドの紹介。")
            if not self.bot.db.users.is_in(id=ctx.author.id):
                e.add_field(name="story", value="最初は必ずこのコマンドを使ってください。")
            elif user == 0:
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

    async def _info(self, ctx):
        e = discord.Embed(title="このbotの情報", description=f"bot version:{self.bot.version}")
        e.add_field(name="導入サーバー数", value=f"{len(self.bot.guilds)} servers")
        e.add_field(name="ユーザー数", value=f"{len(self.bot.users)} users")
        e.add_field(name="チャンネル数", value=f"{len(list(self.bot.get_all_channels()))} channels")
        e.add_field(name="このゲームを遊んでくれている人の数", value=len(self.bot.db.users.get_all()))
        await ctx.send(embed=e)

    @slash_commands.command(description="このbotの情報")
    async def info(self, inter):
        await self._info(inter)
    
    @commands.command("info")
    async def c_info(self, ctx):
        await self._info(ctx)

def setup(bot):
    bot.add_cog(Help(bot))