import os
import json
import argparse  # The argparse module’s support for command-line
                 # interfaces is built around an instance of class named argparse.ArgumentParser.


def getReadbleJsonTree(json_documet) -> str:
    return json.dumps(json_documet, indent=4)


def parseInfo() -> argparse.Namespace:
    # The ArgumentParser.add_argument() method attaches individual argument specifications to the parser.
    # It supports positional arguments, options that accept values, and on/off flags:

    parse = argparse.ArgumentParser(
        prog='MyProgram',
        prefix_chars='-',
        epilog='На улице rain, на душе pain',
        description = 'Parser for labratory three in POSU'
    )

    # Let's declare the possible arguments
    parse.add_argument('-p', '--pid', action='store_true')  # Process PID             (The argument with no values)
    parse.add_argument('-u', '--uid', action='store_true')  # User's UID              (The argument with no values)
    parse.add_argument('-g', '--gid', action='store_true')  # GID of the user's group (The argument with no values)

    # Dictionary with values of environment variables                                 (At least one argument)
    parse.add_argument('-e', '--env', nargs='+', type=str)

    return parse.parse_args()  # The parse_args() method runs the parser and
                               # places the extracted data in a argparse.Namespace object.
                               # So, we can refer to the processed arguments


def main():
    json_documet = {}  # Object for storing the structure of a json document

    incoming_info = parseInfo()  # The incoming information will be processed by the parser and transmitted to incoming_info

    if incoming_info.pid is True:  # If the --pid argument was caught
        json_documet['pid'] = os.getpid()  # add it to the json document

    if incoming_info.uid is True:
        json_documet['uid'] = os.getuid()

    if incoming_info.gid is True:
        json_documet['gid'] = os.getuid()

    if incoming_info.env is not None:
        environment = {}
        for env_var in incoming_info.env:
            environment[env_var.upper()] = os.environ.get(env_var.upper(), 'Not found')
        json_documet['env'] = environment

    return getReadbleJsonTree(json_documet)


if __name__ == "__main__":
    print(main())
