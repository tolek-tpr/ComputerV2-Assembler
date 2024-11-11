import unittest
from memory import buildMemoryMap, buildAddress, referenceLabels, expandToMemory

class TestTokenizeFunction(unittest.TestCase):

    def test_building_some_addresses(self):
        self.assertEqual(buildAddress(0, 0), 0)
        self.assertEqual(buildAddress(0, 1), 1)
        self.assertEqual(buildAddress(1, 0), 64)
        self.assertEqual(buildAddress(1, 1), 65)

    def test_build_memory_map(self):
        intermediate = [
            [None, "NOP", []],
            [".someLabel", None, []],
            [None, "LDI", ["R1", "12345"]],
            [".PAGE:2", None, []],
            [".someOtherLabel", None, []],
            [None, "MST", ["12345", "67890"]]
        ]
        expected = {
            ".someLabel": "1",
            ".someOtherLabel": "128"
        }
        labels = buildMemoryMap(intermediate)
        self.assertEqual(labels, expected)

    def test_reference_labels(self):
        intermediate = [
            [None, "NOP", []],
            [".someLabel", None, []],
            [None, "LDI", ["R1", ".someLabel"]],
            [".PAGE:2", None, []],
            [".someOtherLabel", None, []],
            [None, "MST", ["12345", ".someOtherLabel"]]
        ]
        labels = {
            ".someLabel": "1",
            ".someOtherLabel": "128"
        }
        expected = [
            [None, "NOP", []],
            [".someLabel", None, []],
            [None, "LDI", ["R1", "1"]],
            [".PAGE:2", None, []],
            [".someOtherLabel", None, []],
            [None, "MST", ["12345", "128"]]
        ]
        referenced = referenceLabels(intermediate, labels)
        self.assertEqual(referenced, expected)

    def test_expand_to_memory(self):
        intermediate = [
            [None, "HLT", []],
            [".someLabel", None, []],
            [".PAGE:1", None, []],
            [None, "HLT", []],
            [None, "HLT", []],
            [".someOtherLabel", None, []],
            [".PAGE:3", None, []],
            [".yetAnotherLabel", None, []]
        ]
        expected = [
            [None, "HLT", []], # page 0, offset 0
            [".someLabel", None, []], # ignored
            [None, "NOP", []], # page 0, offset 1
            [None, "NOP", []], # page 0, offset 2
            [None, "NOP", []], # page 0, offset 3
            [".PAGE:1", None, []], # backfilled page 0
            [None, "HLT", []], # page 1, offset 0
            [None, "HLT", []], # page 1, offset 1
            [".someOtherLabel", None, []], # ignored
            [None, "NOP", []], # page 1, offset 2
            [None, "NOP", []], # page 1, offset 3
            [None, "NOP", []], # page 2, offset 0
            [None, "NOP", []], # page 2, offset 1
            [None, "NOP", []], # page 2, offset 2
            [None, "NOP", []], # page 2, offset 3
            [".PAGE:3", None, []], # backfilled page 1 and 2
            [".yetAnotherLabel", None, []] # ignored
        ]
        sparse = expandToMemory(intermediate, 4)
        self.assertEqual(sparse, expected)

if __name__ == '__main__':
    unittest.main()