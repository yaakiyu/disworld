"""import dislash

def EasyMenu(name:str, description:str, **options) -> dislash.SelectMenu:
    opt = [dislash.SelectOption(k,v) for k,v in options.items()]
    menu = dislash.SelectMenu(
        custom_id=name,
        placeholder=description,
        options=opt
    )
    return menu

def EasyButton(label, id, color="green"):
    color = getattr(dislash.ButtonStyle, color, None)
    if not color:
        raise KeyError("存在しない色です。")
    return dislash.ActionRow(
        dislash.Button(style=color, label=label, custom_id=id)
    )"""