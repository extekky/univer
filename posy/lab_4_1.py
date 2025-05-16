import sys
import subprocess
import signal
import json
import os


def handle_sigusr1(signum, frame):
    if child_process is not None:
        child_process.terminate()
        print("Процесс завершен SIGUSR1")
        sys.exit(0)


signal.signal(signal.SIGUSR1, handle_sigusr1)  # Ловим сигнал

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <command> [args...]")
        sys.exit(1)

    cmd = sys.argv[1:-1] if sys.argv[-2] == '<' else sys.argv[1:]
    input_file = sys.argv[-1] if sys.argv[-2] == '<' else None

    try:
        if input_file:
            with open(input_file, 'r') as f:
                child_process = subprocess.Popen(cmd, stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            child_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = child_process.communicate()

        result = {
            "name": cmd[0],
            "return_code": child_process.returncode,
            "stdout": stdout.decode(),
            "stderr": stderr.decode()
        }

        if child_process.returncode < 0:
            result["signal"] = signal.Signals(-child_process.returncode).name

        print(json.dumps(result, indent=4))
    except FileNotFoundError:
        print(f"Command '{cmd[0]}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
