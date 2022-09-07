# Disworld core - Bot

from __future__ import annotations

from typing import Callable

from inspect import iscoroutinefunction
import os

from discord.ext import commands
import discord

from aiohttp import ClientSession
import aiomysql


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("intents", discord.Intents.all())
        super().__init__(*args, **kwargs)
        self._session: ClientSession | None = None
        self.mode: int = 0

    version: str = "0.1.1b"
    version_info: tuple[int, int, int, str] = (0, 1, 1, "beta")
    pool: aiomysql.Pool


    @property
    def session(self):
        if self._session is None or self._session.is_closed:
            self._session = ClientSession()
        return self._session

    async def setup_hook(self):
        # loading first cog
        if self.mode != 2:
            await self.load_extension("cogs._first")
        else:
            await self.load_extension("cogs._special")
            self.dispatch("full_ready")

        self.print("connecting Mysql...", mode="system")
        self.pool = await aiomysql.create_pool(
            host=os.environ["MYSQL_HOST"], port=int(os.environ["MYSQL_PORT"]),
            user=os.environ["MYSQL_USERNAME"], password=os.environ["MYSQL_PASSWORD"],
            db=os.environ["MYSQL_DBNAME"], loop=self.loop, autocommit=True
        )

    def print(self, *args, **kwargs):
        args = [a for a in args] + ["\033[0m"]
        kwargs["sep"] = ""
        if kwargs.get("mode"):
            args = [f"\033[0m[\033[92m{kwargs.get('mode')}\033[0m]\033[93m"] + args
            del kwargs["mode"]
        print("[SystemLog]\033[93m", *args, **kwargs)

    async def lock_checker(
        self, ctx: commands.Context, story_number: int = -1,
        version_lock: str = ""
    ):
        if version_lock:
            if self.version == version_lock:
                await ctx.send("まだこのコマンドを使うことはできません。")

    async def execute_sql(
        self, sql: str | Callable,
        _injects: tuple | None = None, _return_type: str = "",
        **kwargs
    ):
        "SQL文をMySQLにて実行します。"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if iscoroutinefunction(sql):
                    return await sql(cursor, **kwargs)
                elif callable(sql):
                    raise ValueError("sql parameter must be async function.")
                await cursor.execute(sql, _injects)
                if _return_type == "fetchall":
                    return await cursor.fetchall()
                elif _return_type == "fetchone":
                    return await cursor.fetchone()
