import unittest
from compilation import compileLine, compileJump

class TestTokenizeFunction(unittest.TestCase):

    def test_compile_jump(self):
        compiled = compileJump("2", "JIZ")
        expected = "0101100000000000\n0110000100000010"
        self.assertEqual(compiled, expected)

    def test_compile_line(self):
        self.assertEqual(compileLine([None, "NOP", []]), "0000000000000000")
        self.assertEqual(compileLine([None, "HLT", []]), "0000100000000000")
        self.assertEqual(compileLine([None, "LDI", ["R3", "4"]]), "0001001100000100")
        self.assertEqual(compileLine([None, "LDI", ["R3", "4"]]), "0001001100000100")

if __name__ == '__main__':
    unittest.main()