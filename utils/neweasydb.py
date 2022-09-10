# Disworld - NewEasyDB

from __future__ import annotations

import sqlite3

from typing import Optional


class EasyDB():
    def __init__(self, path: str = ":memory:"):
        # ConnectionとCursorの指定
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()

        #Tableオブジェクトの準備
        self.__init_tables__()

    def __init_tables__(self):
        # テーブルオブジェクトを作成し、setattrする。
        for v in self.do("select name from SQLITE_MASTER where type='table' ORDER BY name"):
            pass

    def do(self, content, *, commit: Optional[bool] = False):
        # SQL文を実行する。
        result = self.cur.execute(content)
        if commit:
            self.conn.commit()
        return result
