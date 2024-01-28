# disworld - item

from typing import Any
import discord
from discord.ext import commands

from orjson import loads

from core import Bot


CATEGORIES = [
    ["武器", 4, "weapon"],
    ["防具", 4, "armor"],
    ["アクセサリ", 100, "accessory"],
    ["便利アイテム", 100, "item"],
    ["素材", 100, "material"]
]


class CategorySelect(discord.ui.Select):
    def __init__(self, ctx: commands.Context, bot: Bot):
        super().__init__(placeholder="カテゴリを選択...")
        self.ctx = ctx
        self.bot = bot
        for i in range(len(CATEGORIES)):
            if CATEGORIES[i][1] <= self.bot.db.user[self.ctx.author.id]["Story"]:
                self.add_option(label=CATEGORIES[i][0], value=str(i))

    async def callback(self, interaction: discord.Interaction):
        itemdata = loads(self.bot.db.item[self.ctx.author.id]["Data"])
        result = []
        selected = int(self.values[0])
        for k, v in itemdata.items():
            item = self.bot.itemdata[int(k)]
            if item["type"] == CATEGORIES[selected][2]:
                result.append(f"{item['name']} - {v}個")
        if not result:
            content = "このカテゴリのアイテムをなにも持っていません。"
        else:
            content = "```\n" + "\n".join(result) + "```"
        view = discord.ui.View()
        view.add_item(BackButton(self.ctx, self.bot))
        await interaction.response.edit_message(
            embed=discord.Embed(title=f"{self.ctx.author}の所持{CATEGORIES[selected][0]}一覧", description=content),
            view=view
        )


class BackButton(discord.ui.Button):
    def __init__(self, ctx, bot):
        super().__init__(style=discord.ButtonStyle.red, label="カテゴリ選択に戻る")
        self.ctx = ctx
        self.bot = bot

    async def callback(self, interaction) -> Any:
        ...


class Item(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(description="自分の持っているアイテムの確認をします。")
    async def item(self, ctx: commands.Context):
        await self.bot.lock_checker(ctx, 4, 0.2)

        e = discord.Embed(title="所持アイテム一覧", description="カテゴリを選択してください。")
        view = discord.ui.View()
        view.add_item(CategorySelect(ctx, self.bot))
        await ctx.reply(embed=e, view=view)


async def setup(bot: Bot):
    await bot.add_cog(Item(bot))