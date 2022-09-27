# Disworld core - Bot

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from inspect import iscoroutinefunction, cleandoc
from traceback import TracebackException
import os

from discord.ext import commands
import discord

from aiohttp import ClientSession
import aiomysql

import data
import utils

from .data_cache import DataController


class MyTree(discord.app_commands.CommandTree):
    async def on_error(
        self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError
    ):
        channel = interaction.client.get_channel(794842052184506398)
        assert isinstance(channel, discord.TextChannel)
        error_message = "".join(
            TracebackException.from_exception(error).format()
        )

        print("\033[31m" + error_message + "\033[0m")
        await channel.send(
            cleandoc(f"""発生サーバー：{getattr(interaction.guild, 'name')}(ID:{getattr(interaction.guild, 'id')})
                発生チャンネル：{getattr(interaction.channel, "name")}(ID:{getattr(interaction.channel, 'id')})
                発生ユーザー：{interaction.user}(ID:{interaction.user.id})
                発生コマンド：{getattr(interaction.command, "name")}"""),
            embed=utils.ErrorEmbed("エラー", f"```py\n{error_message}\n```")
        )
        await interaction.response.send_message("エラーが発生しました。")

class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("intents", discord.Intents.all())
        self.mode: int = kwargs.pop("mode", 0)
        super().__init__(*args, tree_cls=MyTree, **kwargs)
        self.db = DataController(self)
        self._session: ClientSession | None = None

    version: str = "0.1.1b"
    version_info: tuple[int, int, int, str] = (0, 1, 1, "beta")
    version_number: float = 0.1
    pool: aiomysql.Pool
    db: DataController
    storydata = data.storydata
    talkdata = data.talkdata
    commandsdata = data.commandsdata
    fielddata = data.fielddata
    itemdata = data.itemdata
    owner_ids: list[int]

    @property
    def session(self):
        "セッションを返す。"
        if self._session is None or self._session.closed:
            self._session = ClientSession()
        return self._session

    async def setup_hook(self):
        self.print("connecting Mysql...", mode="system")
        self.pool = await aiomysql.create_pool(
            host=os.environ["MYSQL_HOST"], port=int(os.environ["MYSQL_PORT"]),
            user=os.environ["MYSQL_USERNAME"], password=os.environ["MYSQL_PASSWORD"],
            db=os.environ["MYSQL_DBNAME"], loop=self.loop, autocommit=True
        )

        # load first cog
        if self.mode != 2:
            await self.load_extension("cogs._first")
        else:
            await self.load_extension("cogs._special")

    async def on_ready(self):
        self.owner_ids = [
            693025129806037003,  # yaakiyu
            696950076207005717,  # DrEleven
            705399971062612011,  # hard Smoothyさん
            575221859642114059,  # mksuke123さん
            667319675176091659,  # takkunさん
            573836903091273729,  # きのたこさん
            884692310166761504,  # mc_fdcさん
        ]

    def print(self, *args, **kwargs):
        "Botの情報をコンソールに出力します。modeキーワード引数があるとそれも考慮します。"
        args = [a for a in args] + ["\033[0m"]
        kwargs.setdefault("sep", "")
        if kwargs.get("mode"):
            args = [f"\033[0m[\033[92m{kwargs.get('mode')}\033[0m]\033[93m"] + args
            del kwargs["mode"]
        print("[SystemLog]\033[93m", *args, **kwargs)

    async def lock_checker(
        self, ctx: commands.Context, story_number: int = -1,
        version_lock: float = 0.0
    ):
        "ユーザーがコマンドを使えるかどうかを判定します。"
        if (
            version_lock
            and self.version_number > version_lock
            and ctx.author.id not in self.owner_ids
        ):
            await ctx.send(embed=utils.ErrorEmbed(
                "エラー",
                "まだこのコマンドは研究段階です。もうしばらく待ってください..."
            ))
            raise utils.SpecialError()
        if ctx.author.id not in self.db.user:
            await ctx.send(embed=utils.ErrorEmbed(
                "エラー",
                "あなたはゲームを始めていません！storyコマンドでゲームを開始してください！"
            ))
            raise utils.SpecialError()
        if (
            story_number != -1
            and self.db.user[ctx.author.id]["Story"] < story_number
        ):
            await ctx.send(embed=utils.ErrorEmbed(
                "エラー",
                "あなたはまだこのコマンドを使う条件を満たしていないようです..."
            ))
            raise utils.SpecialError()

    reT = TypeVar("reT")

    async def execute_sql(
        self, sql: str | Callable[..., reT],
        _injects: tuple | None = None, _return_type: str = "",
        **kwargs
    ) -> None | tuple | reT:
        "SQL文をMySQLにて実行します。"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if iscoroutinefunction(sql):
                    return await sql(cursor, **kwargs)
                await cursor.execute(sql, _injects)
                if _return_type == "fetchall":
                    return await cursor.fetchall()
                elif _return_type == "fetchone":
                    return await cursor.fetchone()
