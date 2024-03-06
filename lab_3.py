import os
import sys
import json
import argparse  # The argparse module’s support for command-line
                 # interfaces is built around an instance of class named argparse.ArgumentParser.
                 # doc: https://docs.python.org/3/library/argparse.html

def getReadbleJsonTree(json_document) -> str:
    return json.dumps(json_document, indent=4)


def parseInfo() -> argparse.Namespace:
    # The ArgumentParser.add_argument() method attaches individual argument specifications to the parser.
    # It supports positional arguments, options that accept values, and on/off flags:

    parse = argparse.ArgumentParser(
        prog='MyProgram',
        prefix_chars='-',
        epilog='На улице rain, на душе pain',
        description = 'A parser for laboratory work on the discipline POSU'
    )

    # Let's declare the possible arguments
    parse.add_argument('-p', '--pid', action='store_true')  # Process PID             (The argument with no values)
    parse.add_argument('-u', '--uid', action='store_true')  # User's UID              (The argument with no values)
    parse.add_argument('-g', '--gid', action='store_true')  # GID of the user's group (The argument with no values)

    # Values of environment variables                             (Only one argument, but can be called many times)
    parse.add_argument('-e', '--env', nargs=1, action='extend')

    # Scanning a directory                                                                      (Only one argument)
    parse.add_argument('-d', '--dir', nargs=1)

    # What positions should be display if there are any           (Only one argument, but can be called many times)
    parse.add_argument('-i', '--itm', dest='pos', nargs=1, action='extend', type=int)

    # Unlimited number of positional arguments                                          (Unlimited number of items)
    parse.add_argument('massive',  nargs='*', action='extend', type=int)

    # Output the contents of a file or input stream                                             (Only one argument)
    parse.add_argument('-f', '--file',  type=argparse.FileType('r'))

    return parse.parse_args()  # The parse_args() method runs the parser and
                               # places the extracted data in a argparse.Namespace object.
                               # So, we can refer to the processed arguments


def main():
    json_document = {}  # Object for storing the structure of a json document

    incoming_info = parseInfo()  # The incoming information will be processed
                                 # by the parser and transmitted to incoming_info

    if incoming_info.pid is True:  # If the --pid argument was caught
        json_document['pid'] = os.getpid()  # add it to the json document

    if incoming_info.uid is True:
        json_document['uid'] = os.getuid()

    if incoming_info.gid is True:
        json_document['gid'] = os.getuid()

    if incoming_info.env is not None:
        json_document['env'] = {
            env_var.upper(): os.environ.get(env_var.upper(), 'Not found')
            for env_var in incoming_info.env
        }

    if incoming_info.dir is not None:
        try:
            json_document['dir'] = os.listdir(incoming_info.dir[-1])
        except FileNotFoundError:
            json_document['dir'] = f"Directory '{incoming_info.dir[-1]}' not found"

    if incoming_info.pos is not None and incoming_info.massive is not None:
        json_document['pos'] = [
            value for i, value in enumerate(incoming_info.massive)
            if i in incoming_info.pos
        ]

    if incoming_info.file is not None:
        if incoming_info.file.name == '<stdin>':
            from_stdin = []
            try:
                while True:
                    from_stdin.append(sys.stdin.readline().strip())
            except KeyboardInterrupt:
                json_document['file'] = from_stdin
        else:
            json_document['file'] = [line.strip() for line in incoming_info.file.readlines() if line.strip()]

    return getReadbleJsonTree(json_document)


if __name__ == "__main__":
    print(main())
