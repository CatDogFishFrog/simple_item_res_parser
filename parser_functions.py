import re, os, codecs
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

app = AppBuilder(path = resource_path("1mini_interface.xml"))

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
    print_parsed_items(parse_folder_items(app.PathVar.get()+"/media/scripts"))
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
    print_parsed_recipe(parse_folder_recipe(app.PathVar.get()+"/media/scripts"))
    app.Label_Output.config(text="Готово. Файл з рецептами створено поруч із цією програмою")

# -------------------------------- Функціонал --------------------------------

def print_parsed_items(items_list:dict, output_path=''): #Виводить в файл масив з предметами у готовий файл локалізації
    with codecs.open(output_path+'ItemName_UA.txt', 'w', encoding='Windows-1251') as output_file:
        output_file.write('ItemName_UA = {')
        for key in items_list:
            for item in items_list[key]:
                if type(item) == str:
                    output_file.write('\n\t'+item)
                else:
                    output_file.write(f'\n\tItemName_{key}.{item[0]} = "{item[1]}",')
        output_file.write('\n}')

def print_parsed_recipe(recipe_list:dict, output_path=''):
    with codecs.open(output_path+'Recipes_UA.txt', 'w', encoding='Windows-1251') as output_file:
        output_file.write('Recipes_UA = {')
        for item in recipe_list:
            if item.startswith('--') or (item == ''):
                output_file.write('\n\t'+item)
            else:
                output_file.write(f'\n\tRecipe_{item.replace(" ", "_")} = "{item}",')
        output_file.write('\n}')

def parse_folder_items(folder_path:str): # Обробляє директорію на Item
    items_arr = {}
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            if os.path.isfile(f'{folder_path}/{item}'):
                try:
                    with codecs.open(f'{folder_path}/{item}', 'r', encoding='utf-8') as file:
                        text = file.read()
                    search = re.search(r'module\s+(\S+)', text)
                    if search == None: continue
                    new_items_arr = parse_items(text)
                    if new_items_arr == []: continue
                    module_name = search.group(1)
                    if module_name in items_arr:
                        items_arr[module_name].extend(['', f'--{item[:-4]}'])
                    else:
                        items_arr[module_name] = ['', f'--{item[:-4]}']
                    items_arr[module_name].extend(new_items_arr)

                except Exception as e:
                    with codecs.open('error_log.txt', 'a', encoding='utf-8') as log:
                        log.write(f'\nПомилка при парсингу Файлу на items. Файл: "{folder_path}/{item}"\n{e.args}\n\n{e.with_traceback}\n')
            else:
                try:
                    new_items_arr = parse_folder_items(f'{folder_path}/{item}')
                    for key in new_items_arr:
                        if key in items_arr:
                            items_arr[key].extend(new_items_arr[key])
                        else:
                            items_arr[key] = new_items_arr[key]
                except Exception as e:
                    with codecs.open('error_log.txt', 'a', encoding='utf-8') as log:
                        log.write(f'\nПомилка при парсингу Директорії на items. Директорія: "{folder_path}/{item}"\n{e.args}\n\n{e.with_traceback}\n')
    return items_arr

def parse_folder_recipe(folder_path:str): # Обробляє директорію на Recipe
    recipe_arr = []
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            if os.path.isfile(f'{folder_path}/{item}'):
                try:
                    with codecs.open(f'{folder_path}/{item}', 'r', encoding='utf-8') as file:
                        text = file.read()
                    new_recipe_arr = parse_recipe(text)
                    if new_recipe_arr == []: continue
                    recipe_arr.extend(['', f'--{item[:-4]}'])
                    recipe_arr.extend(new_recipe_arr)
                except Exception as e:
                    with codecs.open('error_log.txt', 'a', encoding='utf-8') as log:
                        log.write(f'\nПомилка при парсингу Файлу на recipes. Файл: "{folder_path}/{item}"\n{e.args}\n\n{e.with_traceback}\n')
            else:
                try:
                    recipe_arr.extend(parse_folder_recipe(f'{folder_path}/{item}'))
                except Exception as e:
                    with codecs.open('error_log.txt', 'a', encoding='utf-8') as log:
                        log.write(f'\nПомилка при парсингу Директорії на recipes. Директорія: "{folder_path}/{item}"\n{e.args}\n\n{e.with_traceback}\n')
    return recipe_arr

def parse_items(text): # Обробляє один файл на Item
    result = []
    for match in re.finditer(r'item\s+(?P<technical_name>[^\n]+)\s*\{[^}]*DisplayName\s*=\s*(?P<display_name>[^,\n]+)', text):
        result.append([match.group('technical_name').strip(), match.group('display_name').strip()])
    return result

def parse_recipe(text): # Обробляє один файл на Recipe
    result = []
    for match in re.finditer(r'recipe\s+(?P<recipe_name>[^\n]+)', text):
        result.append(match.group('recipe_name').strip())
    return result

app.connect_callbacks(globals())
app.mainloop()