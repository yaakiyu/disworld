# disworld - equipment

from orjson import loads

from discord.ext import commands
import discord

from core import Bot
import utils


class Equip(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _equiplist(self, ctx):
        # 装備を表示する関数
        u_equip = self.bot.db.equipment[ctx.author.id]
        u_item = loads(self.bot.db.item[ctx.author.id]["Data"])

        embed = discord.Embed(title="あなたの装備一覧", description=" ")
        namelist = ["武器", "武器2", "防具", "アクセサリ"]
        for n, equip in enumerate(u_equip):
            if n == 0 or equip == 0:
                continue
            val = self.bot.itemdata[u_item[str(equip)]]["name"]
            embed.add_field(name=namelist[n-1], value=val)

    async def _equipset(self, ctx, args: list[str]):
        # 装備するものを選択する関数
        u_equip = self.bot.db.equipment[ctx.author.id]
        u_item = loads(self.bot.db.item[ctx.author.id]["Data"])
        e = discord.Embed(title="変更する装備を選んでください", description=" ")
        menu = utils.EasyMenu(name="choice_e_set",description="変更する装備箇所",options={["武器", "1"],["武器2", "2"],["防具", "3"],["アクセサリー", "4"]})
        namelist = ["武器", "武器2", "防具", "アクセサリ"]
        for i, m in enumerate(u_equip):
            if i == 0 or m == 0:
                continue
            val = self.bot.itemdata[u_item[str(m)]]["name"]
            e.add_field(name=namelist[i-1], value=val)

    async def _equiprm(self, ctx, args: list[str]):
        # 装備を削除するものを選択する関数
        u_equip = self.bot.db.equipment[ctx.author.id]
        u_item = loads(self.bot.db.item[ctx.author.id]["Data"])
        e = discord.Embed(title="削除する装備を選んでください", description=" ")
        menu = utils.EasyMenu(name="choice_e_set",description="変更する装備箇所",options={["武器", "1"],["武器2", "2"],["防具", "3"],["アクセサリー", "4"]})
        namelist = ["武器", "武器2", "防具", "アクセサリ"]
        for i, m in enumerate(u_equip):
            if i == 0 or m == 0:
                continue
            val = self.bot.itemdata[u_item[str(m)]]["name"]
            e.add_field(name=namelist[i-1], value=val)

    @commands.hybrid_command(description="装備を付け外しします。")
    async def equip(self, ctx: commands.Context, *, arg=None):
        await self.bot.lock_checker(ctx, 6, 0.2)

        if ctx.author.id not in self.bot.db.equipment:
            self.bot.db.equipment.insert((ctx.author.id, 0, 0, 0, 0))
        if arg is None:
            # 装備を表示
            return await self._equiplist(ctx)
        args = arg.split()
        if args[0] == "set":
            # 装備をセット
            await self._equipset(ctx, args)
        if args[0] in ["view", "list"]:
            # 装備を表示
            await self._equiplist(ctx)
        if args[0] in ["del", "remove", "rm", "lift", "delete", "takeoff", "unset",
                       "unequip"]:
            # 装備を解除
            await self._equiprm(ctx, args)


async def setup(bot: Bot):
    await bot.add_cog(Equip(bot))
