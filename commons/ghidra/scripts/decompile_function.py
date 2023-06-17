"""Python 2 script for decompiling a function"""


# pylint: skip-file
# flake8: noqa

import sys

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor


def main():
    function_name = getScriptArgs()[0]
    if not function_name:
        exit(1)

    program = getCurrentProgram()
    decompiler = DecompInterface()
    decompiler.openProgram(program)

    function = getGlobalFunctions(function_name)[0]

    results = decompiler.decompileFunction(function, 0, ConsoleTaskMonitor())
    code = results.getDecompiledFunction().getC()

    print(code)


if __name__ == "__main__":
    main()
