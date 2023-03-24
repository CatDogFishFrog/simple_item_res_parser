import os, parse_items, parse_recipe
import sys
from formation import AppBuilder
from tkinter import filedialog

# -------------------------------- Інтерфейс --------------------------------

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

app = AppBuilder(path = resource_path("mini_interface.xml"))

app.Frame_1._root().resizable(False, False)
app.Frame_1._root().title('item-recipe parser')
app.Frame_1._root().iconbitmap(resource_path('media/zombie-pixel-art.ico'))


def open_inp_path(event=None):
    app.PathVar.set(filedialog.askdirectory())
    if not os.path.exists(app.PathVar.get()):
            app.Label_Output.config(text="Такого мода не існує")
            return
    if not os.path.exists(app.PathVar.get()+"/media/scripts"):
        app.Label_Output.config(text="Не знайдено папку scripts!\nАбо це не мод, або тут немає предметів чи рецептів.")
        return
    app.Label_Output.config(text="Виглядає наче мод. І навіть усі файли на місці.\nВарто спробувати!")

def button_parse_items(event=None):
    try:
        if not os.path.exists(app.PathVar.get()):
            app.Label_Output.config(text="Такого мода не існує")
            return
        if not os.path.exists(app.PathVar.get()+"/media/scripts"):
            app.Label_Output.config(text="Не знайдено папку scripts!\nАбо це не мод, або тут немає предметів чи рецептів.")
            return
    except Exception:
        app.Label_Output.config(text="Якийсь проблемний шлях до моду.\nАбо ви його просто не вказали...")
        return
    parse_items.print_parsed_items(parse_items.parse_folder_items(app.PathVar.get()+"/media/scripts"))
    app.Label_Output.config(text="Готово. Файл з предметами створено поруч із цією програмою")

def button_parse_recipe(event=None):
    try:
        if not os.path.exists(app.PathVar.get()):
            app.Label_Output.config(text="Такого мода не існує")
            return
        if not os.path.exists(app.PathVar.get()+"/media/scripts"):
            app.Label_Output.config(text="Не знайдено папку scripts!\nАбо це не мод, або тут немає предметів чи рецептів.")
            return
    except Exception:
        app.Label_Output.config(text="Якийсь проблемний шлях до моду.\nАбо ви його просто не вказали...")
        return
    parse_recipe.print_parsed_recipe(parse_recipe.parse_folder_recipe(app.PathVar.get()+"/media/scripts"))
    app.Label_Output.config(text="Готово. Файл з рецептами створено поруч із цією програмою")

# -------------------------------- Функціонал --------------------------------

app.connect_callbacks(globals())
app.mainloop()