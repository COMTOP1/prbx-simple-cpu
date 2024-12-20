import math
import unittest

from sections.memory import Memory


class TestMemory(unittest.TestCase):
    def test_memory_init_invalid_negative(self):
        with self.assertRaises(ValueError):
            Memory(-1)

    def test_memory_init_invalid_positive(self):
        with self.assertRaises(ValueError):
            Memory(70000)

    def test_memory_8_bit_insert_valid(self):
        memory = Memory(int(math.pow(2, 8)))
        memory.insert(2, 43)
        memory.insert(5, 87)

    def test_memory_8_bit_insert_invalid_index(self):
        memory = Memory(int(math.pow(2, 8)))
        with self.assertRaises(IndexError):
            memory.insert(-1, 1)
        with self.assertRaises(IndexError):
            memory.insert(256, 1)

    def test_memory_8_bit_insert_invalid_value(self):
        memory = Memory(int(math.pow(2, 8)))
        with self.assertRaises(ValueError):
            memory.insert(1, -1)
        with self.assertRaises(ValueError):
            memory.insert(56, 256)

    def test_memory_8_bit_get_valid(self):
        memory = Memory(int(math.pow(2, 8)))
        memory.insert(2, 43)
        memory.insert(5, 87)
        self.assertEqual(memory.get(2), 43)
        self.assertEqual(memory.get(5), 87)

    def test_memory_8_bit_get_invalid_index(self):
        memory = Memory(int(math.pow(2, 8)))
        with self.assertRaises(IndexError):
            memory.get(-1)
        with self.assertRaises(IndexError):
            memory.get(256)

    def test_memory_16_bit_insert_valid(self):
        memory = Memory(int(math.pow(2, 16)))
        memory.insert(2, 43)
        memory.insert(5, 87)

    def test_memory_16_bit_insert_invalid_index(self):
        memory = Memory(int(math.pow(2, 16)))
        with self.assertRaises(IndexError):
            memory.insert(-1, 1)
        with self.assertRaises(IndexError):
            memory.insert(70000, 1)

    def test_memory_16_bit_insert_invalid_value(self):
        memory = Memory(int(math.pow(2, 16)))
        with self.assertRaises(ValueError):
            memory.insert(1, -1)
        with self.assertRaises(ValueError):
            memory.insert(56, 256)

    def test_memory_16_bit_get_valid(self):
        memory = Memory(int(math.pow(2, 16)))
        memory.insert(2, 43)
        memory.insert(5, 87)
        self.assertEqual(memory.get(2), 43)
        self.assertEqual(memory.get(5), 87)

    def test_memory_16_bit_get_invalid_index(self):
        memory = Memory(int(math.pow(2, 16)))
        with self.assertRaises(IndexError):
            memory.get(-1)
        with self.assertRaises(IndexError):
            memory.get(70000)


if __name__ == '__main__':
    unittest.main()
