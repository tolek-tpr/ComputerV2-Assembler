import unittest
from parsing import tokenizeLine, tokenizeProgram

class TestTokenizeFunction(unittest.TestCase):
    
    def test_empty_line(self):
        self.assertEqual(tokenizeLine(""), [None, None, []])

    def test_label(self):
        self.assertEqual(tokenizeLine(".someLabel"), [".someLabel", None, []])

    def test_page(self):
        self.assertEqual(tokenizeLine(".PAGE:1"), [".PAGE:1", None, []])

    def test_opcode_without_operands(self):
        self.assertEqual(tokenizeLine("NOP"), [None, "NOP", []])

    def test_opcode_with_one_operand(self):
        self.assertEqual(tokenizeLine("LDI R1, 12345"), [None, "LDI", ["R1", "12345"]])

    def test_opcode_with_two_operands(self):
        self.assertEqual(tokenizeLine("MST 12345, 67890"), [None, "MST", ["12345", "67890"]])

    def test_nonexistent_opcode(self):
        self.assertEqual(tokenizeLine("?#! 12345"), [None, None, []])

    def test_tokenize_program(self):
        input = "NOP\n.someLabel\nLDI R1, 12345\nMST 12345, 67890".split("\n")
        expected = [
            [None, "NOP", []],
            [".someLabel", None, []],
            [None, "LDI", ["R1", "12345"]],
            [None, "MST", ["12345", "67890"]]
        ]
        output = tokenizeProgram(input)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()