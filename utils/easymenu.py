import dislash

def EasyMenu(name:str, description:str, **options) -> dislash.SelectMenu:
    opt = [dislash.SelectOption(k,v) for k,v in options.items()]
    menu = dislash.SelectMenu(
        custom_id=name,
        placeholder=description,
        options=opt
    )
    return menu