import csv, os, json
file = 'C:/Users/USER/Documents/Python_Scripts/nii/file.json'

"""Предполагается, что файлы user1,2,3 будут находится в той же директории,
что и json"""

BASE_DIR =  os.path.dirname(os.path.abspath(file)) #находим базовую директорию
users = [x for x in os.listdir(BASE_DIR) if x.endswith(".txt")
        or x.endswith(".csv")] # проверяем тип файла

with open(file, 'r') as f:
    json_data = json.load(f)

for user in users:
    with open(os.path.join(BASE_DIR, user), 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            """
            каждому элементу строки назначаем переменную
            """
            module, name, function = row
            for item in json_data['commands']:
                """
                если все сходится -  пропускаем
                """
                if (item['module'] == module and item['name'] == name
                    and item['function'] == function and
                    {'user': user[:-4]} not in item['param']):

                    continue

                """
                удаляем лишнее, если такое имеется
                """
                if (row is None and {'user': user[:-4]} in item['param']):

                    json_data['commands'].pop({'param': [{'user': user[:-4]}],
                      'name': name,
                      'function': function,
                      'module': module
                    })

                """
                если что-то не сходится - добавляем элемент
                """

                if (item['module'] != module or
                    item['name'] != name or item['function'] != function
                    or {'user': user[:-4]} not in item['param']):

                    json_data['commands'].append({'param': [{'user': user[:-4]}],
                                          'name': name,
                                          'function': function,
                                          'module': module
                                        })
                    break

with open(os.path.join(BASE_DIR, "file.json"), 'w') as f:
    json.dump(json_data, f, indent=2)
