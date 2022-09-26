# disworld - equipment

from orjson import loads

from discord.ext import commands
import discord

from core import Bot
import utils


class Equip(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_group(description="装備を付け外しします。")
    async def equip(self, ctx: commands.Context):
        await self.bot.lock_checker(ctx, 6, 0.2)

        if ctx.author.id not in self.bot.db.equipment:
            self.bot.db.equipment.insert((ctx.author.id, 0, 0, 0, 0))

        if not ctx.invoked_subcommand:
            await ctx.send("使い方が違います。")

    @equip.command("remove", description="装備を解除します。", aliases=[
        "del", "rm", "lift", "delete", "takeoff", "unset", "unequip"
    ])
    async def _equip_rm(self, ctx: commands.Context):
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

    @equip.command("list",
        description="現在の装備を確認します。", aliases=["view"])
    async def _equip_list(self, ctx):
        u_equip = self.bot.db.equipment[ctx.author.id]
        u_item = loads(self.bot.db.item[ctx.author.id]["Data"])

        embed = discord.Embed(title="あなたの装備一覧", description=" ")
        namelist = ["武器", "武器2", "防具", "アクセサリ"]
        for n, equip in enumerate(u_equip):
            if n == 0 or equip == 0:
                continue
            val = self.bot.itemdata[u_item[str(equip)]]["name"]
            embed.add_field(name=namelist[n-1], value=val)

    @equip.command("set", description="装備をします。", aliases=["equip"])
    async def _equip_set(self, ctx, arg: str):
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


async def setup(bot: Bot):
    await bot.add_cog(Equip(bot))
