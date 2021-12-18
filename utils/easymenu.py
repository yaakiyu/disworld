import dislash

def EasyMenu(name, description, **options):
    opt = [dislash.SelectOption(k,v) for k,v in options.items()]
    menu = dislash.SelectMenu(
        custom_id=name,
        placeholder=description,
        options=opt
    )
    return menu