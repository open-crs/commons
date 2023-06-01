import os
import subprocess
import typing
from enum import Enum

COMMENT_PREFIX = "/* WARNING"
REPORT_START_LINE = "INFO  SCRIPT"
REPORT_FINISH_LINE = "INFO  ANALYZING"


PROJECT_FOLDER = "/tmp/ghidra_projects/"
COMMAND_FMT = (
    "{} " + PROJECT_FOLDER + " {} -import {} -overwrite -postscript {}"
)


class AvailableGhidraScripts(Enum):
    DECOMPILE_FUNCTION = "scripts/decompile_function.py"
    EXTRACT_CALLS = "scripts/extract_calls.py"


class GhidraAnalysis:
    __ghidra_headless_path: object
    decompiled_code: str
    calls: typing.Set[str]

    def __init__(self, ghidra_headless_path: str, filename: str) -> None:
        self.__ghidra_headless_path = ghidra_headless_path
        self.filename = filename
        self.decompiled_code = ""
        self.calls = set()

        self.__ensure_project_folder()

    def __ensure_project_folder(self) -> None:
        if not os.path.isdir(PROJECT_FOLDER):
            os.mkdir(PROJECT_FOLDER)

    def __run_headless_ghidra(
        self, script: AvailableGhidraScripts, argv: typing.List[str] = None
    ) -> typing.List[str]:
        analysis_script = os.path.join(os.getcwd(), script.value)

        ghidra_command = COMMAND_FMT.format(
            self.__ghidra_headless_path,
            self.filename,
            self.filename,
            analysis_script,
        ).split(" ")
        if argv:
            ghidra_command.extend(argv)

        try:
            process = subprocess.run(
                ghidra_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )

            raw_output = process.stdout.decode("utf-8").splitlines()

            return list(self.__extract_script_result(raw_output))
        except subprocess.CalledProcessError:
            return None

    def __extract_script_result(
        self, raw_output: typing.List[str]
    ) -> typing.Generator[str, None, None]:
        is_script_output = False
        for line in raw_output:
            if line.startswith(REPORT_START_LINE):
                is_script_output = True
                continue

            if line.startswith(REPORT_FINISH_LINE):
                break

            if is_script_output:
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

    def __process_decompiled_code(self, lines: typing.List[str]) -> None:
        code = "\n".join(lines)

        code = self.__replace_undefs(code)
        code = self.__replace_longs(code)
        code = self.__replace_double_lines(code)
        code = self.__replace_comments_for_pycparser(code)

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
