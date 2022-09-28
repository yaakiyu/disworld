# disworld - item

import discord
from discord.ext import commands
import utils
from orjson import loads

from core import Bot


class Item(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(description="自分の持っているアイテムの確認をします。")
    async def item(self, ctx: commands.Context):
        await self.bot.lock_checker(ctx, 5, 0.2)

        udata = loads(self.bot.db.item[ctx.author.id]["Data"])
        embedpages = []
        em = discord.Embed(title="アイテム一覧", description="page:1")
        for id, count in udata.items():
            itemdata = self.bot.itemdata[int(id)]
            em.add_field(name=itemdata["name"], value=f"個数:{count}個")
            if len(em.fields) == 20:
                embedpages.append(em)
                em = discord.Embed(title="アイテム一覧", 
                                   description=f"page:{len(embedpages)+1}")
        if len(em.fields):
            embedpages.append(em)
        if len(embedpages) == 0:
            return await ctx.send(embed=utils.ErrorEmbed("エラー", "まだあなたは何のアイテムも持っていません。"))
        if len(embedpages) == 1:
            return await ctx.send(embed=embedpages[0])
        nowpage = 0
        buttons = [utils.EasyButton("前へ", "prev"), utils.EasyButton("次へ", "next")]
        msg = await ctx.send(embed=embedpages[0])

    """
        on_click = msg.create_click_listener(timeout=60)

        @on_click.matching_id("prev")
        async def on_previous_button(inter):
            global nowpage
            nowpage = (nowpage + len(embedpages) - 1) % len(embedpages)
            await inter.reply(embed=embedpages[nowpage], components=buttons)

        @on_click.matching_id("next")
        async def on_next_button(inter):
            global nowpage
            nowpage = (nowpage + 1) % len(embedpages)
            await inter.reply(embed=embedpages[nowpage], components=buttons)

        @on_click.timeout
        async def on_timeout():
            await msg.edit(components=[])
    """


async def setup(bot: Bot):
    await bot.add_cog(Item(bot))