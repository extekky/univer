# Пример использования stas@ubuntu:~$ python3 /home/stas/wtf.py /home/stas/Downloads
import json
import stat
import sys
import os
import pwd


def type_entity(file_path):
    file_stat = os.stat(file_path)
    file_mode = file_stat.st_mode

    if stat.S_ISREG(file_mode):
        return "normal"
    elif stat.S_ISDIR(file_mode):
        return "dir"
    elif stat.S_ISCHR(file_mode):
        return "char"
    elif stat.S_ISBLK(file_mode):
        return "block"
    else:
        return "unknown"


def get_structure_data(my_path):
    file_tree = {
        'type': type_entity(my_path),
        'name': os.path.basename(my_path),
        'children': []
    }
    for entity in os.scandir(my_path):
        if entity.is_file():
            file_tree['children'].append({
                'type': type_entity(entity),
                'name': os.path.basename(entity),
                'size': os.path.getsize(entity)
            })

        if entity.is_dir():
            file_tree["children"].append(get_structure_data(entity.path))

    return file_tree


def write():
    json_data = json.dumps(get_structure_data(path), indent=3)
    print(json_data)

    current_user = pwd.getpwuid(os.getuid())
    username = current_user.pw_name

    output_file_path = f'/home/{username}/output.json'
    with open(output_file_path, 'w') as output_file:
        output_file.write(json_data)

    print('\nФайл сохранен по адресу:', output_file_path)


if len(sys.argv) < 2:
    print("Пример использования\nstas@ubuntu:~$ python3 /home/stas/wtf.py /home/stas/Downloads")
else:
    path = sys.argv[1]
    if not os.path.isdir(path):
        print("Invalid path")
    else:
        write()
