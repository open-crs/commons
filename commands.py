"""Module for running OS commands."""

import subprocess


def get_command_output(command: str) -> str:
    argv = command.split(" ")

    return subprocess.check_output(argv).decode("utf-8")
