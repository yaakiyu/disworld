# disworld - develop

from typing import Optional

from discord.ext import commands
from discord import app_commands
import discord

import orjson

from core import Bot


dev_guilds = (discord.Object(a) for a in [699120642796028014, 794079140462460979])


class Develop(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(
        description="管理者専用DB操作コマンド"
    )
    @app_commands.guilds(*dev_guilds)
    @app_commands.describe(content="実行するSQL文")
    async def db(self, interaction, content: str):
        if interaction.author.id in self.bot.owner_ids:
            res = await self.bot.execute_sql(content, return_type="fetchall")
            await interaction.response.send_message(
                f"結果: {res}", ephemeral=True
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
        if not inter.user.id in self.bot.owner_ids:
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
    async def checkdata(
        self, inter: discord.Interaction, table_name: str, cid: int
    ):
        if not inter.user.id in self.bot.owner_ids:
            return await inter.response.send_message(
                "あなたはこのコマンドを実行する権限がありません。", ephemeral=True
            )
        res = await self.bot.execute_sql(
            f"SELECT * FROM {table_name} WHERE Id = %s", (cid,),
            return_type="fetchall"
        )
        await inter.response.send_message(
            str(res), ephemeral=True
        )

    @app_commands.command(
        description="(管理者専用)人にものを与えます"
    )
    @app_commands.guilds(*dev_guilds)
    @app_commands.describe(user="与える対象", thing="与えるもの", count="与える個数")
    async def give(
        self, inter: discord.Interaction, user: discord.User, thing: str, count: int
    ):
        if not inter.user.id in self.bot.owner_ids:
            return await inter.response.send_message(
                "あなたはこのコマンドを実行する権限がありません。", ephemeral=True
            )
        if thing == "money":
            self.bot.db.user[user.id]["Money"] += count
            thing = "お金"
        elif thing.isdigit():
            itemdata = orjson.loads(self.bot.db.item[user.id]["Data"])
            itemdata[thing] = itemdata.get(thing, 0) + count
            self.bot.db.item[user.id]["Data"] = orjson.dumps(itemdata)
        else:
            await inter.response.send_message("与えるものは`money`もしくはアイテムIDで記入してください。")
        await inter.response.send_message(
            f"{user} に {thing} を {count} 個与えました。"
        )


async def setup(bot: Bot):
    await bot.add_cog(Develop(bot))
