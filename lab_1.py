import json
import os.path
from typing import Any, Dict, List

MY_FILE = 'input.json'


def transformData(DATA: Any) -> List[Any]:
    transformed_data = []
    for item in DATA:
        if isinstance(item, list):
            transformed_data.append(item[1::2])
        elif isinstance(item, dict):
            new_dict = {
                key.upper() if isinstance(key, str) else key: value
                for key, value in item.items()
            }
            transformed_data.append(new_dict)
        elif isinstance(item, str):
            transformed_data.append(item[:len(item) // 2])
        else:
            transformed_data.append(item)
    return transformed_data


def getReadableJsonFile(DATA: Any) -> str:
    return json.dumps(DATA, indent=4)


def main() -> str:
    if not os.path.exists(MY_FILE):
        return f"Can't find {MY_FILE}"
    try:
        with open(MY_FILE, 'r') as file:
            DATA = json.load(file)
    except Exception as e:
        return f"Error reading file: {e}"
    return getReadableJsonFile(transformData(DATA))


if __name__ == "__main__":
    print(main())
