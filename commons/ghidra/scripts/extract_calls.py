"""Python 2 script for dumping all the called functions

This script uses Ghidra for traversing the function of an ELF, getting all the
called functions and printing them on screen.
"""

# pylint: skip-file
# flake8: noqa

from ghidra.util.task import TaskMonitor


def main():
    function_manager = currentProgram.getFunctionManager()
    functions = function_manager.getFunctions(True)

    called_functions = set()
    for function in functions:
        current_called_functions = function.getCalledFunctions(
            TaskMonitor.DUMMY
        )
        for called_function in current_called_functions:
            called_functions.add(called_function)

    for called_function in called_functions:
        print(called_function)


if __name__ == "__main__":
    main()
