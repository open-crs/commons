import os
import subprocess
import typing
from enum import Enum

import docker

IMAGE_TAG = "ghidra"

COMMENT_PREFIX = "/* WARNING"
REPORT_START_LINE = "INFO  SCRIPT"
REPORT_FINISH_LINE = "INFO  ANALYZING"

GHIDRA_PATH_IN_CONTAINER = "/opt/ghidra/support/analyzeHeadless"
SCRIPTS_MOUNT_IN_FOLDER = "/scripts"
BINARY_PATH_IN_CONTAINER = "binary"
COMMAND_FMT = (
    f"{GHIDRA_PATH_IN_CONTAINER} /tmp {BINARY_PATH_IN_CONTAINER} -import"
    f" {BINARY_PATH_IN_CONTAINER} -overwrite -postscript {{}}"
)


class AvailableGhidraScripts(Enum):
    DECOMPILE_FUNCTION = "decompile_function.py"
    EXTRACT_CALLS = "extract_calls.py"


class GhidraAnalysis:
    __docker_client: docker.client
    _container: typing.Any
    decompiled_code: str
    calls: typing.Set[str]

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.decompiled_code = ""
        self.calls = set()

        self.__docker_client = docker.from_env()

        self.__start_container()

    def __start_container(self) -> typing.List[str]:
        host_scripts_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "scripts"
        )

        self._container = self.__docker_client.containers.run(
            IMAGE_TAG,
            command="tail -f /dev/null",
            tty=True,
            auto_remove=True,
            detach=True,
            volumes={
                self.filename: {
                    "bind": "/" + BINARY_PATH_IN_CONTAINER,
                    "mode": "rw",
                },
                host_scripts_folder: {
                    "bind": SCRIPTS_MOUNT_IN_FOLDER,
                    "mode": "rw",
                },
            },
        )

    def __run_headless_ghidra(
        self, script: AvailableGhidraScripts, argv: typing.List[str] = None
    ) -> typing.List[str]:
        analysis_script = os.path.join(SCRIPTS_MOUNT_IN_FOLDER, script.value)
        ghidra_command = COMMAND_FMT.format(
            analysis_script,
        ).split(" ")
        if argv:
            ghidra_command.extend(argv)

        _, output = self._container.exec_run(
            ghidra_command,
            workdir="/",
        )
        raw_output = output.decode("utf-8").splitlines()

        return list(self.__extract_script_result(raw_output))

    def __extract_script_result(
        self, raw_output: typing.List[str]
    ) -> typing.Generator[str, None, None]:
        is_script_output = False
        for line in raw_output:
            if line.startswith(REPORT_START_LINE):
                is_script_output = True
                continue

            if is_script_output:
                if line.startswith(REPORT_FINISH_LINE):
                    break

                yield line

    def __preprocess_call(
        self, calls: typing.List[str]
    ) -> typing.Generator[str, None, None]:
        for call in calls:
            call = call.strip()

            if "::" in call:
                yield call.split("::")[1]
            else:
                yield call

    def __process_decompiled_code(self, lines: typing.List[str]) -> str:
        code = "\n".join(lines)

        code = self.__replace_undefs(code)
        code = self.__replace_longs(code)
        code = self.__replace_double_lines(code)
        code = self.__replace_comments_for_pycparser(code)

        return code

    def __replace_undefs(self, code: str) -> None:
        return code.replace("undefined4", "int").replace("undefined", "char")

    def __replace_longs(self, code: str) -> None:
        return code.replace("char8", "long")

    def __replace_double_lines(self, code: str) -> None:
        return code.replace("\n\n", "\n")

    def __replace_comments_for_pycparser(self, code: str) -> None:
        # pycparser won't be able to parse lines with comments.
        no_comments_code = []
        for line in code.splitlines():
            if COMMENT_PREFIX not in line:
                no_comments_code.append(line)

        return "\n".join(no_comments_code)

    def decompile_function(self, function_name: str) -> str:
        analysis_report = self.__run_headless_ghidra(
            AvailableGhidraScripts.DECOMPILE_FUNCTION, [function_name]
        )

        return self.__process_decompiled_code(analysis_report)

    def extract_calls(self) -> str:
        analysis_report = self.__run_headless_ghidra(
            AvailableGhidraScripts.EXTRACT_CALLS
        )

        return self.__preprocess_call(analysis_report)
