# Disworld core - Bot

from __future__ import annotations

from discord.ext import commands
from aiohttp import ClientSession


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._session: ClientSession | None = None
        self.mode: int = 0

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

    def print(self, *args, **kwargs):
        args = [a for a in args] + ["\033[0m"]
        kwargs["sep"] = ""
        if kwargs.get("mode"):
            args = [f"\033[0m[\033[92m{kwargs.get('mode')}\033[0m]\033[93m"] + args
            del kwargs["mode"]
        print("[SystemLog]\033[93m", *args, **kwargs)