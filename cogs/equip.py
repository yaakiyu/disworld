from discord.ext import commands
from dislash import slash_commands, OptionParam

class Equip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _equip(self, ctx, arg):
        # バージョンロック
        if self.bot.version == "0.2":
            return await ctx.send("主人公はまだ装備の仕方を知らない...")
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
        if args[0] in ["del", "remove", "rm", "lift", "delete"]:
            # 装備を解除
            await self._equiprm(ctx, args)

    async def _equiplist(self, ctx):
        # 装備を表示する関数
        u_equip = self.bot.db.equipment[ctx.author.id][0]
        u_item = self.bot.db.item[ctx.author.id][0]

    async def _equipset(self, ctx, args: list):
        # 装備する関数
        pass

    async def _equiprm(self, ctx, args: list):
        # 装備を削除する関数
        pass

    @commands.command("equip")
    async def c_equip(self, ctx, *, arg=None):
        return await self._equip(ctx, arg)

    @slash_commands.command(description="装備を確認したり、装備したりします。")
    async def equip(self, inter, arg:str = OptionParam("None", desc="操作")):
        return await self._equip(inter, (arg if arg != "None" else None))

def setup(bot):
    bot.add_cog(Equip(bot))