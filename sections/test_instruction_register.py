import unittest

from sections.instruction_register import InstructionRegister


class TestInstructionRegister(unittest.TestCase):
    def setUp(self):
        self.instruction_register = InstructionRegister()

    def test_instruction_register_valid(self):
        tests = {(2, 2), (817, 817)}
        for inserted_value, expected_value in tests:
            self.instruction_register.insert(inserted_value)
            self.assertEqual(self.instruction_register.get(), expected_value)

    def test_instruction_register_error(self):
        with self.assertRaises(ValueError):
            self.instruction_register.insert(70000)

if __name__ == '__main__':
    unittest.main()
