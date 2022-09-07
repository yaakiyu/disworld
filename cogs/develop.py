# RT - develop

from typing import Optional

from discord.ext import commands
from discord import app_commands
import discord

dev_guilds = (discord.Object(a) for a in [699120642796028014, 794079140462460979])

class Develop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        description="管理者専用DB操作コマンド"
    )
    @app_commands.guilds(*dev_guilds)
    @app_commands.describe(content="実行するSQL文")
    async def db(self, interaction, content: str):
        if interaction.author.id in self.bot.owner_ids:
            await interaction.response.send_message(
                "結果:" + str(self.bot.db.do(content)), ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "あなたはこのコマンドを実行する権限がありません。", ephemeral=True
            )

    @app_commands.command(
        description="管理者専用ヘルプコマンド"
    )
    @app_commands.guilds(*dev_guilds)
    @app_commands.describe(command="詳しいヘルプをみたいコマンド名")
    async def admin_help(
        self, inter: discord.Interaction,
        command: Optional[str] = None
    ):
        if not inter.author.id in self.bot.owner_ids:
            return await inter.response.send_message(
                "あなたはこのコマンドを実行する権限がありません。", ephemeral=True
            )
        if command is None:
            e = discord.Embed(
                title="help", 
                description="dbコマンド：データベースを操作します。\n"
                "checkdataコマンド：データベースからIDで検索します。\n"
                "reload_dataコマンド：コマンドやストーリーなどのデータを再読込みします。"
            )
        elif command == "db":
            e = discord.Embed(
                title="dbコマンドの詳細",
                description="SQL構文でデータベースを操作します。"
            )
        elif command == "checkdata":
            e = discord.Embed(
                title="checkdataコマンドの詳細",
                description="`checkdata [テーブル名] [ID]`で検索できます。"
                "idカラムが存在しないテーブルは対応していません。"
            )
        else:
            e = discord.Embed(title="コマンドが見つかりませんでした。")
        await inter.response.send_message(embed=e, ephemeral=True)

    @app_commands.command(
        description="管理者専用データを検索"
    )
    @app_commands.guilds(*dev_guilds)
    @app_commands.describe(table_name="テーブル名", cid="検索するID")
    async def checkdata(self, inter, table_name: str, cid: int):
        if not inter.author.id in self.bot.owner_ids:
            return await inter.reply("あなたはこのコマンドを実行する権限がありません。", ephemeral=True)
        data = self.bot.db.get_table(table_name)
        if len(data[int(cid)]) == 0:
            return await inter.reply("No data found.")
        await inter.reply(dict(zip(data.values, data[int(cid)][0])), ephemeral=True)


async def setup(bot):
    await bot.add_cog(Develop(bot))
