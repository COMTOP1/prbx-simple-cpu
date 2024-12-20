import unittest

from sections.accumulator import Accumulator


class TestAccumulator(unittest.TestCase):
    def setUp(self):
        self.accumulator = Accumulator()

    def test_accumulator_valid(self):
        tests = {(2, 2), (220, 220)}
        for inserted_value, expected_value in tests:
            self.accumulator.insert(inserted_value)
            self.assertEqual(self.accumulator.get(), expected_value)

    def test_accumulator_error(self):
        with self.assertRaises(ValueError):
            self.accumulator.insert(256)

if __name__ == '__main__':
    unittest.main()
