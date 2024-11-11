FORMATS = {
    "NOP": ("00000", "00000000000"),
    "HLT": ("00001", "00000000000"),
    "LDI": ("00010", "REG", "IMM_8"),
    "MOV": ("00011", "REG", "REG", "00000"),
    "ADD": ("00100", "REG", "REG", "REG", "00"),
    "SUB": ("00101", "REG", "REG", "REG", "00"),
    "BIT": ("00110", "REG", "REG", "REG", "BITS"),
    "MST": ("00111", "REG", "IMM_8"),
    "MLD": ("01000", "REG", "IMM_8"),
    "SPU": ("01001", "REG", "00000000"),
    "SPO": ("01010", "REG", "00000000"),
    "PPL": ("01011", "000", "IMM_8"),
    "JMP": ("01100", "BITS", "IMM_8"),
    "CAL": ("01101", "000", "IMM_8"),
    "RET": ("01110", "00000000000"),
    "PLD": ("01111", "REG", "IMM_8"),
    "PST": ("10000", "REG", "IMM_8")
}

ALIAS = {
    "JIZ": "JMP",
    "JINZ": "JMP",
    "JIC": "JMP",
    "NOT": "BIT",
    "AND": "BIT",
    "OR": "BIT",
    "XOR": "BIT"
}

BITS = {
    # Branch logic
    "JMP": "000", "JIZ": "001",
    "JINZ": "010", "JIC": "011",
    # ALU logic
    "NOT": "00", "AND": "01",
    "OR": "10", "XOR": "11"
}