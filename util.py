from errors import AssemblerError

PAGE_SIZE = 64

def toDecimal(number: str) -> int:
    if number[0:2] == "0b":  # binary
        return int(number[2:], 2)
    if number[0:2] == "0x":  # hex
        return int(number[2:], 16)
    if number[0:2] == "0o":  # octal
        return int(number[2:], 8)
    if number[0:2] == "0d":  # decimal
        return int(number[2:], 10)
    return int(number)

def toBinary(number: int, length: int) -> str:
    if number < 0:
        number = 2 ** length + number
    result = str(bin(number))[2:]
    if len(result) > length:
        raise AssemblerError(f"Number too long for {length} bits: {number}")
    return result.zfill(length)

