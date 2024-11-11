import formats

from typing import List
from errors import AssemblerError
from parsing import tokenizeProgram
from memory import buildMemoryMap, referenceLabels, expandToMemory
from compilation import compileProgram

# CLEAN UP

def removeComments(lines: List[str]) -> List[str]:
    formatLines = []
    for line in lines:
        if not (line.startswith("//")) and line:
            formatLines.append(line)
    return formatLines

# Files

def writeFile(file: str, lines: List[str]) -> None:
    with open(file, "w") as f:
        for line in lines: f.write(line + "\n") 

def readFile(file: str) -> List[str]:
    with open(file, "r") as f:
        lines = [line.strip() for line in f]
    return removeComments(lines)

# Main thing

def assemble(program: List[str]) -> List[str]:
    program = removeComments(program)
    intermediate = tokenizeProgram(program)
    labels = buildMemoryMap(intermediate)
    linked = referenceLabels(intermediate, labels)
    sparse = expandToMemory(linked)
    compiled = compileProgram(sparse)
    return formatAssembly(compiled)

def assembleFile(file: str) -> None:
    lines = readFile(file)
    lines = assemble(lines)

    file = file.split(".")[0] + ".mhc"
    writeFile(file, lines)

def formatAssembly(lines: List[str]) -> List[str]:
    return [line[0:8] + " " + line[8:16] for line in lines]

file = input("Assembly file: ")
assembleFile(file)