import formats

from typing import List
from util import toDecimal, PAGE_SIZE

def buildAddress(page: int, offset: int) -> int:
    return (page << 6) + (offset & 0x3f) # binary 00111111

def buildMemoryMap(intermediate: List) -> dict[str]:
    if (intermediate[0] == ".PAGE:0"):
        intermediate.pop(0)

    offset = 0
    page = 0
    labels = {}

    for tokens in intermediate:
        label, opcode, _ = tokens

        if label:
            if label[0:6] == ".PAGE:":
                page = toDecimal(label[6:])
                offset = 0
            else:
                labels[label] = str(buildAddress(page, offset))

        if opcode: 
            doLoadPage = formats.ALIAS.get(opcode, None) == "JMP"
            offset += 2 if doLoadPage else 1

    return labels

def referenceLabels(intermediate: List, labels: dict[str]) -> List:
    for line, intermediateLine in enumerate(intermediate):
        _, _, operands = intermediateLine
        if operands:
            for n, operand in enumerate(operands):
                if operand and operand[0:1] == ".":
                    print(f"Found operand label {operand}, referencing {labels.get(operand)}")
                    intermediate[line][2][n] = labels.get(operand, "undefined")
                    # TODO: throw when label reference not found
    return intermediate

def expandToMemory(intermediate: List, pageSize = PAGE_SIZE) -> List:
    sparse = []
    page = 0
    offset = 0

    for intermediateLine in intermediate:
        label, opcode, _ = intermediateLine
        
        if label and label[0:6] == ".PAGE:":
            nextPage = toDecimal(label[6:])
            for _ in range(nextPage - page):
                for _ in range(pageSize - 1 - offset):
                    sparse.append([None, "NOP", []])
                offset = 0
                page += 1
        
        if opcode: 
            doLoadPage = formats.ALIAS.get(opcode, None) == "JMP"
            offset += 2 if doLoadPage else 1
        
        sparse.append(intermediateLine)

    return sparse