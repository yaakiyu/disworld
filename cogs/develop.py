from discord.ext import commands
import discord
import dislash
from dislash import slash_commands, Option

dev_guilds = [794079140462460979, 914391660786503690, 903866784887762995]

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
            await inter.reply("結果:" + self.bot.db.do(content))
        else:
            await inter.reply("あなたはこのコマンドを実行する権限がありません。", ephemeral=True)

    @slash_commands.command(
        guild_ids=dev_guilds,
        description="管理者専用ヘルプコマンド",
        options=[Option("command", "詳しいヘルプを見たいコマンド名", required=False)]
    )
    async def admin_help(self, inter, command=None):
        if not inter.author.id in self.bot.owner_ids:
            return await inter.reply("あなたはこのコマンドを実行する権限がありません。", ephemeral=True)
        if command is None:
            e = discord.Embed(title="help", description="dbコマンド：データベースを操作します。")
        elif command == "db":
            e = discord.Embed(title="dbコマンドの詳細", description="SQL構文でデータベースを操作します。")
        elif command == "checkdata":
            e = discord.Embed(title="checkdataコマンドの詳細", description="`checkdata [テーブル名] [ID]`で検索できます。idカラムが存在しないテーブルは対応していません。")
        else:
            e = discord.Embed(title="コマンドが見つかりませんでした。")
        await inter.reply(embed=e)
    
    @slash_commands.command(
        guild_ids=dev_guilds,
        description="管理者専用データを検索",
        options=[
            Option("table_name", "データを検索したいテーブルを選択", required=True, 
            choices=[
                dislash.OptionChoice("users", 1),
                dislash.OptionChoice("items", 2)
            ]),
            Option("id", "検索したいID", dislash.OptionType.INTEGER, required=True)
        ]
    )
    async def checkdata(self,inter,table,cid):
        if not inter.author.id in self.bot.owner_ids:
            return await inter.reply("あなたはこのコマンドを実行する権限がありません。", ephemeral=True)
        await inter.reply(self.bot.db.get_table(table)[cid])


def setup(bot):
    bot.add_cog(Develop(bot))