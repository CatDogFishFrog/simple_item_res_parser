import re, os, codecs

def print_parsed_recipe(recipe_list:dict, output_path=''):
    with codecs.open(output_path+'Recipes_UA.txt', 'w', encoding='Windows-1251') as output_file:
        output_file.write('Recipes_UA = {')
        for item in recipe_list:
            if item.startswith('--') or (item == ''):
                output_file.write('\n\t'+item)
            else:
                output_file.write(f'\n\tRecipe_{item.replace(" ", "_")} = "{item}",')
        output_file.write('\n}')

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

def parse_recipe(text): # Обробляє один файл на Recipe
    result = []
    for match in re.finditer(r'recipe\s+(?P<recipe_name>[^\n]+)', text):
        result.append(match.group('recipe_name').strip())
    return result