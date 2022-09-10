# Disworld utils - easymenu

from typing import Optional

from collections.abc import Callable

import discord


def EasyMenu(
    name: str, description: str, *,
    callback: Optional[Callable] = None, **options
) -> discord.ui.Select:
    opt = [discord.SelectOption(label=k, description=v) for k,v in options.items()]
    menu = discord.ui.Select(
        custom_id=name,
        placeholder=description,
        options=opt
    )
    if callback:
        menu.callback = callback
    return menu


def EasyButton(
    label, id_, color="green", callback: Optional[Callable] = None
) -> discord.ui.Button:
    "簡単にボタンを作ることができます。"
    color = getattr(discord.ButtonStyle, color, None)
    if not color:
        raise ValueError("存在しない色です。")

    button = discord.ui.Button(style=color, label=label, custom_id=id_)

    if callback:
        button.callback = callback
    return button


def EasyView(*items) -> discord.ui.View:
    view = discord.ui.View()
    for i in items:
        view.add_item(i)
    return view
