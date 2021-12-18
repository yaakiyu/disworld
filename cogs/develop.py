from discord.ext import commands
import discord
from dislash import slash_commands, Option

dev_guilds = [794079140462460979, 914391660786503690]

class Develop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_commands.command(
        guild_ids=dev_guilds,
        description="管理者専用DB操作コマンド",
        options=[Option("content", "実行するsql構文", required=True)]
    )
    async def db(self, inter, content):
        if inter.author.id in self.bot.owner_ids:
            self.bot.db.do(content)
        else:
            await inter.reply("あなたはこのコマンドを実行する権限がありません。", ephemeral=True)
    
    @slash_commands.command(
        guild_ids=dev_guilds,
        description="管理者専用ヘルプコマンド",
        options=[Option("command", "詳しいヘルプを見たいコマンド名", required=False)]
    )
    async def admin_help(self, inter, command=None):
        if command is None:
            e = discord.Embed(title="help", description="dbコマンド：データベースを操作します。")
        elif command == "db":
            e = discord.Embed(title="dbコマンドの詳細", description="データベースを操作します。\n基本的な操作は下に示します。")
            e.add_field(name="テーブルの追加", value="")
        else:
            e = discord.Embed(title="コマンドが見つかりませんでした。")
        await inter.reply(embed=e)


def setup(bot):
    bot.add_cog(Develop(bot))