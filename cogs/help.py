from discord.ext import commands
from discord import app_commands
import discord

from core import Bot


class Help(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="ヘルプを表示します。")
    @app_commands.describe(command="ヘルプを表示したいコマンド")
    async def c_help(self, ctx, command: str | None = None):
        if not self.bot.db.users.is_in(id=ctx.author.id):
            self.bot.db.users.add_item(ctx.author.id, "", 0, 0, 0, 0, 0)
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


    @commands.hybrid_command("info", description="botの情報を表示します。")
    async def c_info(self, ctx):
        e = discord.Embed(title="このbotの情報", description=f"bot version:{self.bot.version}", color=0x00ff00)
        e.add_field(name="導入サーバー数", value=f"{len(self.bot.guilds)} servers")
        e.add_field(name="ユーザー数", value=f"{len(self.bot.users)} users")
        e.add_field(name="チャンネル数", value=f"{len(list(self.bot.get_all_channels()))} channels")
        e.add_field(name="このゲームを遊んでくれている人の数", value=len(self.bot.db.users.get_all()))
        await ctx.send(embed=e)


async def setup(bot: Bot):
    await bot.add_cog(Help(bot))
