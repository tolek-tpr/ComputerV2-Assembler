.PAGE:0
LDI R1, 5
JMP .label
OR R2, R1, R0

.label
LDI R3, 4
JIZ .label2

.PAGE:1
XOR R3, R2, R1
.label2
LDI R3, 4