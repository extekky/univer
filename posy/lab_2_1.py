import os
import sys
import stat
import json


def getTypeFile(MY_FILE_PATH) -> str:
    if stat.S_ISCHR(os.stat(MY_FILE_PATH).st_mode):
        return 'char'
    if stat.S_ISDIR(os.stat(MY_FILE_PATH).st_mode):
        return 'dir'
    if stat.S_ISBLK(os.stat(MY_FILE_PATH).st_mode):
        return 'block'
    if stat.S_ISREG(os.stat(MY_FILE_PATH).st_mode):
        return 'normal'


def makeJsonTree(MY_FILE_PATH: str) -> dict:
    dir_name, base_name = os.path.split(MY_FILE_PATH)
    if not base_name:
        base_name = os.path.basename(dir_name)

    tree = {
        'name': base_name,
        'type': getTypeFile(MY_FILE_PATH),
        'children': []
    }

    for what_is_that in os.scandir(MY_FILE_PATH):
        if getTypeFile(what_is_that.path) in ('char', 'normal', 'block'):
            tree['children'].append({
                'name': os.path.basename(what_is_that.path),
                'type': getTypeFile(what_is_that.path),
                'size': os.path.getsize(what_is_that.path)
            })

        if getTypeFile(what_is_that.path) == 'dir':
            tree['children'].append(makeJsonTree(what_is_that.path))

    return tree


def getReadbleJsonTree(JSON_TREE) -> str:
    return json.dumps(JSON_TREE, indent=4)


def main():
    if len(sys.argv) != 2:
        return "Usage: python3 <python_file> <directory_path>"

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        return f"Invalid path: {directory_path}"

    return getReadbleJsonTree(makeJsonTree(directory_path))


if __name__ == "__main__":
    print(main())
