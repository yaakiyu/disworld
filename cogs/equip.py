from discord.ext import commands
import discord
from dislash import slash_commands, OptionParam
import utils
import json

class Equip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _equip(self, ctx, arg):
        if self.bot.version == "0.2":
            # バージョンロック
            return await ctx.send("主人公はまだ装備の仕方を知らない...")
        if not self.bot.db.users.is_in(id=ctx.author.id):
            return await ctx.send("あなたはゲームを始めていません！storyコマンドでゲームを開始してください！")
        if self.bot.db.users[ctx.author.id][0][2] < 6:
            return await utils.RequireFault(ctx)
        if not self.bot.db.equipment.is_in(id=ctx.author.id):
            self.bot.db.equipment.add_item(ctx.author.id, 0, 0, 0, 0)
        if arg is None:
            # 装備を表示
            await self._equiplist(ctx)
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

    async def _equiplist(self, ctx):
        # 装備を表示する関数
        u_equip = self.bot.db.equipment[ctx.author.id][0]
        u_item = json.loads(self.bot.db.item[ctx.author.id][0][1])
        e = discord.Embed(title="あなたの装備一覧", description=" ")
        namelist = ["武器", "武器2", "防具", "アクセサリ"]
        for i, m in enumerate(u_equip):
            if i == 0 or m == 0:
                continue
            val = self.bot.itemdata[u_item[str(m)]]["name"]
            e.add_field(name=namelist[i-1], value=val)

    async def _equipset(self, ctx, args: list):
        # 装備する「ものを選択する」関数（処理を分けた方がよいと判断）
        u_equip = self.bot.db.equipment[ctx.author.id][0]
        u_item = json.loads(self.bot.db.item[ctx.author.id][0][1])
        e = discord.Embed(title="変更する装備を選んでください", description=" ")
        menu = utils.EasyMenu(name="choice_e_set",description="変更する装備箇所",options={["武器", "w1"],["武器2", "w2"],["防具", "am"],["アクセサリー", "ac"]})
        namelist = ["武器", "武器2", "防具", "アクセサリ"]
        for i, m in enumerate(u_equip):
            if i == 0 or m == 0:
                continue
            val = self.bot.itemdata[u_item[str(m)]]["name"]
            e.add_field(name=namelist[i-1], value=val)

    async def _equiprm(self, ctx, args: list):
        # 装備を削除する「ものを選択する」関数（処理を分けた方がよいと判断）
        u_equip = self.bot.db.equipment[ctx.author.id][0]
        u_item = json.loads(self.bot.db.item[ctx.author.id][0][1])
        e = discord.Embed(title="削除する装備を選んでください", description=" ")
        menu = utils.EasyMenu(name="choice_e_set",description="変更する装備箇所",options={["武器", "w1"],["武器2", "w2"],["防具", "am"],["アクセサリー", "ac"]})
        namelist = ["武器", "武器2", "防具", "アクセサリ"]
        for i, m in enumerate(u_equip):
            if i == 0 or m == 0:
                continue
            val = self.bot.itemdata[u_item[str(m)]]["name"]
            e.add_field(name=namelist[i-1], value=val)
        pass

    @commands.command("equip")
    async def c_equip(self, ctx, *, arg=None):
        return await self._equip(ctx, arg)

    @slash_commands.command(description="装備を確認したり、装備したりします。")
    async def equip(self, inter, arg:str = OptionParam("None", desc="操作")):
        return await self._equip(inter, (arg if arg != "None" else None))

def setup(bot):
    bot.add_cog(Equip(bot))