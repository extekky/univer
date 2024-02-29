import os
import json

MY_FILE = 'input.json'  # Таргет


# Существует ли MY_FILE в текущем каталоге
def read_directory():
    return os.path.exists(os.path.join(os.getcwd(), MY_FILE))


# Преобразование файла в структуру json
def create_data():
    with open(MY_FILE) as f:
        json_data = json.load(f)
    return json_data


# Модифицирование
def get_right_json(data):
    new_data = []
    for element in data:
        new_element = element

        if isinstance(element, dict):
            new_element = {key.upper(): value for key, value in element.items()}

        elif isinstance(element, str):
            new_element = element[:len(element) // 2]

        elif isinstance(element, list):
            new_element = element[1::2]

        new_data.append(new_element)
    return new_data


def main():
    if read_directory():
        right_data = get_right_json(create_data())
        output = json.dumps(right_data, indent=4)  # Табуляця в 4 пробела
        print(output)
    else:
        print(f'В текущей директории нет файла {MY_FILE}')


if __name__ == "__main__":
    main()
