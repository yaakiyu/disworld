# disworld - data cache

from typing import TYPE_CHECKING, Any

from copy import copy

from discord.ext import tasks
import aiomysql

if TYPE_CHECKING:
    from .bot import Bot


class Columnlized(tuple):
    "各データ用クラス。getitemの実装をするためだけ。"
    columns: tuple

    def __getitem__(self, item):
        if isinstance(item, str):
            if item not in self.columns:
                raise KeyError("不明なカラム。")
            return super().__getitem__(self.columns.index(item))
        elif isinstance(item, int):
            return super().__getitem__(item)
        raise KeyError("そんなデータないで。")


class DataBaseCache:
    "個々のキャッシュ本体。getitemによるアクセスを可能とする。"
    first_data: Any
    data: Any
    bot: "Bot"
    table_name: str
    columns: tuple

    def __init__(self, table_name: str, bot: "Bot"):
        self.table_name = table_name
        self.bot = bot

    async def async_setup(self) -> None:
        columns = await self.bot.execute_sql(
            f"SHOW COLUMNS FROM {self.table_name}", _return_type="fetchall"
        )
        if not columns:
            raise ValueError("テーブルが存在しない...?")
        self.columns = tuple(x[0] for x in columns)

        data = await self.bot.execute_sql(
            f"SELECT * FROM {self.table_name}", _return_type="fetchall"
        )
        self.data = []
        for i in data:  # type: ignore
            cldata = Columnlized(i)
            cldata.columns = self.columns
            self.data.append(cldata)
        self.data = tuple(self.data)

        self.first_data = copy(self.data)

    def insert(self, data: tuple):
        cldata = Columnlized(data)
        cldata.columns = self.columns
        self.data.append(cldata)

    def __getitem__(self, item: int):
        if item < 1000000:
            return self.data[item]
        if item not in (ids := [i[0] for i in self.data]):
            raise KeyError("そんなデータない。")
        return self.data[ids.index(item)]

    def get_by_id(self, item: int):
        return self.__getitem__(item)


class CacheController:
    user: DataBaseCache
    item: DataBaseCache
    equipment: DataBaseCache

    def __init__(self, bot: "Bot"):
        "キャッシュの初期化。"
        self.bot = bot
        self.user = DataBaseCache("User", bot)
        self.item = DataBaseCache("Item", bot)
        self.equipment = DataBaseCache("Equipment", bot)

    async def async_setup(self):
        "非同期セットアップ。 mysql接続済みの前提で動作します。"
        await self.user.async_setup()
        await self.item.async_setup()
        await self.equipment.async_setup()

        self.saveloop.start()

    @tasks.loop(minutes=1)
    async def saveloop(self):
        "データのセーブをします。"
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                for db in (self.user, self.item, self.equipment):
                    for row in db.data:
                        await self.data_check(db, row, cursor)

    async def data_check(
        self, db: DataBaseCache, row: Columnlized,
        cursor: aiomysql.Cursor
    ):
        if row in db.first_data:
            return
        if row[0] not in (ids := [r[0] for r in db.first_data]):
            # insertする。
            await cursor.execute(
                f"INSERT INTO {db.table_name} VALUES ("
                + ("%s" * len(row.columns)) + ");",
                row
            )
        if db[ids.index(row[0])] != row:
            # updateする。
            await cursor.execute(
                f"UPDATE {db.table_name} SET "
                + ", ".join(f"{i} = %s" for i in row.columns)
                + "WHERE Id = %s",
                row + (row[0],)
            )
