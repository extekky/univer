import sys
import subprocess
import signal
import json

child_processes = []


def handle_sigusr1(signum, frame):
    for process in child_processes:
        process.terminate()
    sys.exit(0)


signal.signal(signal.SIGUSR1, handle_sigusr1)


def run_pipeline(commands, input_file=None):
    global child_processes
    processes = []
    prev_process = None

    for i, command in enumerate(commands):
        cmd = command.split()
        if i == 0 and input_file:
            input_handle = open(input_file, 'r')
        else:
            input_handle = None

        if prev_process:
            input_handle = prev_process.stdout

        if i == len(commands) - 1:
            process = subprocess.Popen(cmd, stdin=input_handle, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            process = subprocess.Popen(cmd, stdin=input_handle, stdout=subprocess.PIPE)

        processes.append(process)
        prev_process = process

    child_processes = processes

    stdout, stderr = processes[-1].communicate()
    return processes, stdout, stderr


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <command> [args...]")
        sys.exit(1)

    args = sys.argv[1:]
    commands = []
    input_file = None

    i = 0
    while i < len(args):
        if args[i] == "<":
            input_file = args[i + 1]
            i += 1
        elif args[i] == "|":
            i += 1
        else:
            command = []
            while i < len(args) and args[i] not in ["<", "|"]:
                command.append(args[i])
                i += 1
            commands.append(' '.join(command))

    processes, stdout, stderr = run_pipeline(commands, input_file)

    result = []
    for process in processes:
        process_info = {
            "name": process.args[0],
            "code": process.returncode
        }
        if process is processes[-1]:
            process_info["output"] = stdout.decode()
            if process.returncode < 0:
                process_info["signal"] = signal.Signals(-process.returncode).name
        result.append(process_info)

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
