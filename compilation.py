import formats

from typing import List
from errors import AssemblerError
from util import toBinary, toDecimal

def compileImmediate(immediate: str, length: int) -> str:
    if immediate[0] == '"':
        return toBinary(ord(immediate[1].replace("@", " ")), length)
    if not immediate[0] in "-0123456789":
        immediate = immediate[1:]
    try:
        immediateindex = toDecimal(immediate)
    except ValueError:
        raise AssemblerError(f"Invalid immediate: {immediate}")
    else:
        return toBinary(immediateindex % (2 ** length), length)

def compileRegister(register: str) -> str:
    if (register[0] in ("$", "R", "r") and len(register) == 2):
        try:
            toDecimal(register[1])
        except ValueError:
            raise AssemblerError(f"Invalid register: {register}")
        if not (toDecimal(register[1]) > 7):
            return toBinary(toDecimal(register[1]), 3)
        else :
            raise AssemblerError(f"Invalid register: {register}")
    else:
        raise AssemblerError(f"Invalid register: {register}")

def compileJump(address: str, opcode: str) -> str:
    result = ""
    addr = toDecimal(address)
    result += ("01011000" + str(toBinary(addr >> 6, 8))) + "\n"
    result +=("01100" + formats.BITS[opcode] + "00" + str(toBinary(addr & 0b00111111, 6)))
    return result

def compileProgram(intermediate: List) -> List[str]:
    output = []
    for intermediateLine in intermediate:
        i = compileLine(intermediateLine).split("\n")
        if (len(i) > 1):
            output.append(i[0])
            output.append(i[1])
            continue
        if (i[0]): 
            output.append(i[0])
    return output

def compileLine(intermediateLine: List) -> str:
    _, opcode, operands = intermediateLine
    if opcode == None:
        return ""

    base = formats.ALIAS.get(opcode, opcode)
    if (base not in formats.FORMATS):
        raise AssemblerError(f"Invalid opcode: {base} {opcode}")

    output = ""
    for operand in formats.FORMATS[base]:
        if (operand == "01100"):
            output += compileJump(operands.pop(0), opcode)
        elif (operand == "REG"):
            output += compileRegister(operands.pop(0)) if operands else "000"
        elif (operand[0:4] == "IMM_"):
            length = int(operand.split("_")[1])
            output += compileImmediate(operands.pop(0), length) if operands else "0" * length
        elif (operand == "BITS"):
            output += formats.BITS[opcode]
        else:
            output += operand

    return output

