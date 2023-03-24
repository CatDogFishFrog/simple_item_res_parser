import re, os, codecs



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

def parse_items(text): # Обробляє один файл на Item
    result = []
    for match in re.finditer(r'item\s+(?P<technical_name>[^\n]+)\s*\{[^}]*DisplayName\s*=\s*(?P<display_name>[^,\n]+)', text):
        result.append([match.group('technical_name').strip(), match.group('display_name').strip()])
    return result