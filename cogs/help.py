from discord.ext import commands
import discord
from dislash import slash_commands, Option

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _help(self, ctx, command):
        if not self.bot.db.users.is_in(id=ctx.author.id):
            self.bot.db.users.add_item(ctx.author.id, "", 0, 0, 0, "")
        user = self.bot.db.users.search(id=ctx.author.id)[0][2]
        if command is None:
            e = discord.Embed(title="Help", description="このbotのコマンドの紹介。")
            for name, values in self.bot.commandsdata.items():
                if values["type"] == "default":
                    e.add_field(name=name, value=values["short"], inline=False)
                elif values["type"] == "story":
                    if values["require"] <= user:
                        e.add_field(name=name, value=values["short"], inline=False)
                elif values["type"] == "story_special":
                    if values["short"](user):
                        e.add_field(name=name, value=values["short"](user), inline=False)
        else:
            e = discord.Embed(title=f"help - {command}", description="** **")
            if command in self.bot.commandsdata.keys():
                values = self.bot.commandsdata[command]
                if values["type"] == "default":
                    e.add_field(name="説明", value=values["description"])
                elif values["type"] == "story":
                    if values["require"] <= user:
                        e.add_field(name="説明", value=values["description"])
                    else:
                        e.add_field(name="説明", value="**__このコマンドの使用条件を満たしていません。__**")
                elif values["type"] == "story_special":
                    if values["description"](user):
                        e.add_field(name="説明", value=values["description"](user))
                    else:
                        e.add_field(name="説明", value="**__このコマンドの使用条件を満たしていません。__**")
            else:
                e.add_field(name="説明", value="コマンドが見つかりませんでした。")
        await ctx.reply(embed=e)

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