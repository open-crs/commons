import subprocess


def execute_command(command: str) -> str:
    argv = command.split(" ")

    return subprocess.check_output(argv).decode("utf-8")
