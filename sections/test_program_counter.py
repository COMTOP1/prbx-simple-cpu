import unittest

from program_counter import ProgramCounter


class TestProgramCounter(unittest.TestCase):
    def setUp(self):
        self.program_counter = ProgramCounter()

    def test_program_counter_enable(self):
        self.assertEqual(self.program_counter.get(), 0)
        self.program_counter.enable()
        self.assertEqual(self.program_counter.get(), 1)

    def test_program_counter_enable_overflow(self):
        self.program_counter.insert(255)
        self.program_counter.enable()
        self.assertEqual(self.program_counter.get(), 0)

    def test_program_counter_insert(self):
        self.program_counter.insert(255)
        self.assertEqual(self.program_counter.get(), 255)

    def test_program_counter_insert_error(self):
        with self.assertRaises(OSError):
            self.program_counter.insert(70000)

if __name__ == '__main__':
    unittest.main()
