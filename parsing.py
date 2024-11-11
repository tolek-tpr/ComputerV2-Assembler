from typing import List
from errors import AssemblerError

import formats

def tokenizeProgram(program: List[str]) -> List:
    output = []
    while len(program) > 0:
        output.append(tokenizeLine(program.pop(0)))
    return output

def tokenizeLine(line: str) -> List:
    tokens = line.replace(",", " ").replace("  ", " ").split()
    label = tokens.pop(0) if len(tokens) > 0 and tokens[0][0:1] == "." else None
    opcode = tokens.pop(0) if len(tokens) > 0 and (tokens[0] in formats.FORMATS or tokens[0] in formats.ALIAS) else None
    # TODO: throw exception when invalid opcode
    operands = tokens if opcode and tokens else []
    # TODO: throw exception when operands don't match those required by opcode
    return [label, opcode, operands]
