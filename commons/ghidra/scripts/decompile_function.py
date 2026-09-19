"""Python 2 script for decompiling a function"""


# pylint: skip-file
# flake8: noqa

import sys

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor


def main():
    args = getScriptArgs()
    if not args:
        print("ERROR: No function name provided")
        return
    
    function_name = args[0]
    program = getCurrentProgram()
    decompiler = DecompInterface()
    decompiler.openProgram(program)

    # Try 1: Find by name (e.g., 'main')
    functions = getGlobalFunctions(function_name)
    function = None

    if functions:
        function = functions[0]
    else:
        # Try 2: Look for any symbol containing 'entry' or 'main'
        symbol_table = program.getSymbolTable()
        for symbol in symbol_table.getAllSymbols(True):
            if symbol.getName() in ["entry", "_start", "main"]:
                function = getFunctionAt(symbol.getAddress())
                if function: break
        
        # Try 3: Pick the first function known to the function manager (if any)
        if not function:
            functions_iter = program.getFunctionManager().getFunctions(True)
            if functions_iter.hasNext():
                function = functions_iter.next()

    if not function:
        print("ERROR: No functions identified in the binary.")
        return

    results = decompiler.decompileFunction(function, 0, ConsoleTaskMonitor())
    if results and results.getDecompiledFunction():
        code = results.getDecompiledFunction().getC()
        print(code)
    else:
        print("ERROR: Decompilation failed for function at {}".format(function.getEntryPoint()))


if __name__ == "__main__":
    main()
